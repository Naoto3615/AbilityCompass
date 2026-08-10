import json
import numpy as np
from django.conf import settings

_client = None


def _get_client():
    """OpenAIクライアントを遅延初期化（APIキー未設定時のエラーを防ぐ）"""
    global _client
    if _client is None:
        from openai import OpenAI
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            return None
        _client = OpenAI(api_key=api_key)
    return _client

EMOTION_LABELS = {5: 'とてもよい', 4: 'まあまあ', 3: 'ふつう', 2: 'すこしつらい', 1: 'とてもつらい'}
HEALTH_LABELS = {3: 'からだがよい', 2: 'ふつう', 1: 'つらい'}


def get_embedding(text: str) -> list:
    """テキストの埋め込みベクトルを取得する"""
    try:
        c = _get_client()
        if not c:
            return []
        response = c.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception:
        return []


def cosine_similarity(a: list, b: list) -> float:
    """コサイン類似度を計算する"""
    a_arr, b_arr = np.array(a), np.array(b)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / (norm_a * norm_b))


def embed_support_record(support_record) -> bool:
    """支援記録をベクトル埋め込みする"""
    from .models import SupportRecordEmbedding
    text = f"""
支援記録 ({support_record.date})
支援内容: {support_record.content}
今日のできた！: {support_record.achievement or ''}
""".strip()

    vector = get_embedding(text)
    if not vector:
        return False

    emb, _ = SupportRecordEmbedding.objects.get_or_create(support_record=support_record)
    emb.set_vector(vector)
    emb.save()
    return True


def search_similar_records(query: str, child, top_k: int = 5) -> list:
    """クエリに類似した支援記録を検索する"""
    from .models import SupportRecordEmbedding
    from daycare.models import SupportRecord

    query_vector = get_embedding(query)
    if not query_vector:
        return list(SupportRecord.objects.filter(child=child).order_by('-date')[:top_k])

    embeddings = SupportRecordEmbedding.objects.filter(
        support_record__child=child
    ).select_related('support_record')

    scored = []
    for emb in embeddings:
        vec = emb.get_vector()
        if vec:
            score = cosine_similarity(query_vector, vec)
            scored.append((score, emb.support_record))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored[:top_k]]


def generate_rag_advice_for_child(child, query: str) -> dict:
    """
    支援員向け: 特定の児童に関する支援記録を元にRAGアドバイスを生成する
    """
    from daycare.models import DevelopmentScore

    relevant_records = search_similar_records(query, child, top_k=5)
    dev_scores = DevelopmentScore.objects.filter(child=child).order_by('-date')[:3]

    context_parts = [f"【対象児童】{child.nickname}"]

    if child.notes:
        context_parts.append(f"【備考・特記事項】{child.notes}")

    if relevant_records:
        context_parts.append("【関連する支援記録】")
        for rec in relevant_records:
            context_parts.append(
                f"・{rec.date} の記録\n"
                f"  支援内容: {rec.content}\n"
                f"  できたこと: {rec.achievement or '未記録'}"
            )

    if dev_scores:
        context_parts.append("【最近の発達スコア（1〜5段階）】")
        for score in dev_scores:
            context_parts.append(
                f"・{score.date}: 集中力={score.focus} / コミュニケーション={score.communication} "
                f"/ 生活習慣={score.daily_living} / 社会性={score.social} / 運動={score.motor}"
            )

    context = "\n".join(context_parts)

    system_prompt = (
        "あなたは障がい者就労支援・放課後デイサービスの専門AIアドバイザーです。\n"
        "支援記録・発達データを元に、対象者の特性を分析し、具体的で実践的なアドバイスを提供してください。\n"
        "回答は支援員が読んでも分かりやすい日本語で、温かく建設的な表現を使ってください。"
    )

    user_message = (
        f"{context}\n\n"
        f"【質問・依頼】\n{query}\n\n"
        "上記の記録を踏まえて、具体的なアドバイスをお願いします。適性職業についても言及してください。"
    )

    try:
        c = _get_client()
        if not c:
            raise Exception("API key not configured")
        response = c.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        advice_text = response.choices[0].message.content
        return {
            'success': True,
            'advice': advice_text,
            'sources': [
                {'date': str(rec.date), 'summary': rec.content[:60]}
                for rec in relevant_records
            ],
        }
    except Exception as e:
        return {
            'success': False,
            'advice': '現在AIアドバイスを生成できません。支援記録を参考に、担当支援員にご相談ください。',
            'sources': [],
        }


def generate_rag_advice_for_user(user_profile, query: str) -> dict:
    """
    利用者向け: ログインユーザー自身の日常記録・プロフィールを元にRAGアドバイスを生成する
    """
    from daily.models import DailyRecord

    recent_records = DailyRecord.objects.filter(
        user=user_profile.user
    ).order_by('-date')[:10]

    disability_map = {'mild': '軽度', 'moderate': '中度', 'other': 'その他'}
    user_type_map = {'adult': '就労を目指す大人', 'child': '児童'}

    context_parts = [
        f"【利用者情報】{user_profile.nickname}",
        f"  利用者種別: {user_type_map.get(user_profile.user_type, '')}",
        f"  障害区分: {disability_map.get(user_profile.disability_level, '')}",
    ]

    if user_profile.desired_career:
        context_parts.append(f"  なりたい職業: {user_profile.desired_career}")

    if user_profile.grade:
        context_parts.append(f"  学年区分: {user_profile.grade}")

    if recent_records:
        context_parts.append("【最近の日常記録（最大10件）】")
        for rec in recent_records:
            emotion_label = EMOTION_LABELS.get(rec.emotion_stamp, 'ふつう')
            health_label = HEALTH_LABELS.get(rec.health_score, 'ふつう')
            context_parts.append(
                f"・{rec.date}: 気持ち={emotion_label} / 体調={health_label}\n"
                f"  できたこと: {rec.did_well or '未記録'}\n"
                f"  むずかしかったこと: {rec.struggled_with or '未記録'}"
            )

    context = "\n".join(context_parts)

    system_prompt = (
        "あなたは障がい者就労支援の専門AIアドバイザーです。\n"
        "利用者本人の日常記録・プロフィールを元に、その人の特性に合った具体的なアドバイスを提供してください。\n"
        "回答はやさしい日本語で、本人が読んでも分かりやすく、励ましのある表現を使ってください。\n"
        "難しい漢字にはふりがなを付けるなど、読みやすさを意識してください。"
    )

    user_message = (
        f"{context}\n\n"
        f"【質問・相談】\n{query}\n\n"
        "上記の記録を踏まえて、具体的なアドバイスをお願いします。"
        "向いている仕事や将来の可能性についても教えてください。"
    )

    try:
        c = _get_client()
        if not c:
            raise Exception("API key not configured")
        response = c.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        advice_text = response.choices[0].message.content
        return {
            'success': True,
            'advice': advice_text,
            'record_count': len(recent_records),
        }
    except Exception as e:
        return {
            'success': False,
            'advice': '現在AIアドバイスを生成できません。担当支援員にご相談ください。',
            'record_count': 0,
        }
