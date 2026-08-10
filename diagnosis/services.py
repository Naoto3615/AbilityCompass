import json
from django.conf import settings

# ─── 診断質問（漢字・ひらがな両対応） ────────────────────────────────────────
DIAGNOSIS_QUESTIONS = [
    # 集中力（3問）
    {
        "id": "q1",
        "category": "focus",
        "text": "同じ作業をずっとくりかえすことができる",
        "emoji": "🔁",
    },
    {
        "id": "q2",
        "category": "focus",
        "text": "好きな作業は時間を忘れて一生懸命できる",
        "emoji": "⏰",
    },
    {
        "id": "q3",
        "category": "focus",
        "text": "最後まであきらめずに作業を続けられる",
        "emoji": "🎯",
    },
    # コミュニケーション力（2問）
    {
        "id": "q4",
        "category": "communication",
        "text": "わからないとき「わかりません」と言える",
        "emoji": "🙋",
    },
    {
        "id": "q5",
        "category": "communication",
        "text": "「おはようございます」「ありがとうございます」のあいさつができる",
        "emoji": "👋",
    },
    # 体力・持続力（2問）
    {
        "id": "q6",
        "category": "endurance",
        "text": "体を動かす仕事が好き",
        "emoji": "💪",
    },
    {
        "id": "q7",
        "category": "endurance",
        "text": "1日中立って仕事をしても疲れにくい",
        "emoji": "🏃",
    },
    # 几帳面さ・正確性（2問）
    {
        "id": "q8",
        "category": "accuracy",
        "text": "ものをきれいに並べたり整理することが好き",
        "emoji": "📦",
    },
    {
        "id": "q9",
        "category": "accuracy",
        "text": "まちがいを見つけることや丁寧にやることが得意",
        "emoji": "🔍",
    },
    # 感情コントロール（2問）
    {
        "id": "q10",
        "category": "emotion_control",
        "text": "うまくできないとき、落ち着いてやり直せる",
        "emoji": "😌",
    },
    {
        "id": "q11",
        "category": "emotion_control",
        "text": "予定が変わっても、パニックになりにくい",
        "emoji": "🧘",
    },
    # 学習意欲・変化への適応（2問）
    {
        "id": "q12",
        "category": "learning",
        "text": "新しいことを教えてもらうのが好き",
        "emoji": "📚",
    },
    {
        "id": "q13",
        "category": "learning",
        "text": "できないことができるようになると嬉しい",
        "emoji": "⭐",
    },
]

SCORE_LABELS = {
    1: "全然あてはまらない",
    2: "あまりあてはまらない",
    3: "どちらとも言えない",
    4: "少しあてはまる",
    5: "とてもあてはまる",
}

SCORE_EMOJIS = {
    1: "😔",
    2: "🤔",
    3: "😐",
    4: "🙂",
    5: "😊",
}

# ─── 仕事タイプ定義 ─────────────────────────────────────────────────────────
JOB_TYPES = [
    {
        "key": "agriculture",
        "name": "農業・園芸系",
        "emoji": "🌱",
        "description": "いちごや野菜を育てたり、植物の世話をする仕事",
        "color": "green",
    },
    {
        "key": "manufacturing",
        "name": "製造・組み立て系",
        "emoji": "🔧",
        "description": "部品を組み立てたり、決まった手順で作業する仕事",
        "color": "blue",
    },
    {
        "key": "cleaning",
        "name": "清掃・環境整備系",
        "emoji": "🧹",
        "description": "建物や施設をきれいに掃除・整理する仕事",
        "color": "sky",
    },
    {
        "key": "food_processing",
        "name": "食品加工系",
        "emoji": "🍱",
        "description": "食べ物を作ったり、袋に入れたりする仕事",
        "color": "orange",
    },
    {
        "key": "service",
        "name": "接客・販売補助系",
        "emoji": "🛒",
        "description": "お店でお客さんのお手伝いや商品を並べる仕事",
        "color": "pink",
    },
]

# ─── 特性ラベル ──────────────────────────────────────────────────────────────
TRAIT_LABELS = {
    "focus": {
        "name": "集中力",
        "emoji": "🔁",
        "desc": "同じ作業をずっと続ける力",
    },
    "communication": {
        "name": "コミュニケーション力",
        "emoji": "👋",
        "desc": "指示を聞いたり報告する力",
    },
    "endurance": {
        "name": "体力・持続力",
        "emoji": "💪",
        "desc": "体を使う仕事を続ける力",
    },
    "accuracy": {
        "name": "几帳面さ・正確性",
        "emoji": "🔍",
        "desc": "ていねいに正確に作業する力",
    },
    "emotion_control": {
        "name": "感情コントロール",
        "emoji": "😌",
        "desc": "落ち着いて対処する力",
    },
    "learning": {
        "name": "学習意欲・適応力",
        "emoji": "📚",
        "desc": "新しいことを覚えようとする力",
    },
}


def get_questions():
    return DIAGNOSIS_QUESTIONS


def get_job_types():
    return JOB_TYPES


def _calc_trait_scores(answers: dict) -> dict:
    """カテゴリごとのスコアを合計する"""
    scores = {trait: 0 for trait in TRAIT_LABELS}
    counts = {trait: 0 for trait in TRAIT_LABELS}
    for q in DIAGNOSIS_QUESTIONS:
        cat = q["category"]
        score = int(answers.get(q["id"], 3))
        scores[cat] = scores.get(cat, 0) + score
        counts[cat] = counts.get(cat, 0) + 1
    avg_scores = {}
    for trait in TRAIT_LABELS:
        cnt = counts.get(trait, 1)
        avg_scores[trait] = round(scores.get(trait, 0) / cnt, 1)
    return avg_scores


def _determine_job_type(trait_scores: dict) -> str:
    """スコアから最も向いている仕事タイプを判定"""
    f = trait_scores.get("focus", 0)
    c = trait_scores.get("communication", 0)
    e = trait_scores.get("endurance", 0)
    a = trait_scores.get("accuracy", 0)
    ec = trait_scores.get("emotion_control", 0)
    l = trait_scores.get("learning", 0)

    job_scores = {
        "agriculture":      e * 0.4 + f * 0.3 + ec * 0.3,
        "manufacturing":    f * 0.4 + a * 0.4 + e * 0.2,
        "cleaning":         e * 0.4 + a * 0.3 + f * 0.3,
        "food_processing":  a * 0.4 + f * 0.3 + e * 0.3,
        "service":          c * 0.4 + ec * 0.3 + l * 0.3,
    }
    return max(job_scores, key=lambda k: job_scores[k])


def analyze_with_ai(answers: dict) -> dict:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        trait_scores = _calc_trait_scores(answers)
        questions_text = "\n".join(
            f"Q{i+1}. {q['text'] if isinstance(q['text'], str) else q['text'].get('kanji', '')}（スコア: {answers.get(q['id'], 3)}/5）"
            for i, q in enumerate(DIAGNOSIS_QUESTIONS)
        )

        prompt = f"""あなたは軽度知的障害のある大人の就労支援の専門家です。
以下は就労支援利用者が答えた自己評価アンケートの結果です（1=あてはまらない、5=よくあてはまる）。

{questions_text}

この結果を分析して、以下のJSON形式で返してください。
文章はやさしい日本語・ひらがな多用でお願いします。

{{
  "strengths": [
    {{"trait": "特性キー", "title": "つよみの名前（10文字以内）", "description": "説明（40文字以内）", "emoji": "絵文字1つ"}},
    {{"trait": "特性キー", "title": "名前", "description": "説明", "emoji": "絵文字"}}
  ],
  "challenges": [
    {{"trait": "特性キー", "title": "かだいの名前（10文字以内）", "description": "説明（40文字以内）", "emoji": "絵文字1つ"}},
    {{"trait": "特性キー", "title": "名前", "description": "説明", "emoji": "絵文字"}}
  ],
  "job_type": "agriculture|manufacturing|cleaning|food_processing|service のどれか",
  "summary": "この人へのはげましのメッセージ（80文字以内、ポジティブ・やさしい言葉で）"
}}

特性キーは focus / communication / endurance / accuracy / emotion_control / learning のどれか。
必ずJSON形式のみを返してください。"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        result['trait_scores'] = trait_scores
        return result

    except Exception:
        return _fallback_analysis(answers)


def _fallback_analysis(answers: dict) -> dict:
    """OpenAI APIが使えない場合のフォールバック分析"""
    trait_scores = _calc_trait_scores(answers)
    job_type = _determine_job_type(trait_scores)

    sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)

    strength_map = {
        "focus": {
            "title": "集中する力",
            "description": "同じ作業をずっと続けられます",
            "emoji": "🔁",
        },
        "communication": {
            "title": "コミュニケーション力",
            "description": "あいさつや報告ができます",
            "emoji": "👋",
        },
        "endurance": {
            "title": "体力・続ける力",
            "description": "体を使う仕事が得意です",
            "emoji": "💪",
        },
        "accuracy": {
            "title": "ていねいさ",
            "description": "正確に作業できます",
            "emoji": "🔍",
        },
        "emotion_control": {
            "title": "落ち着く力",
            "description": "困ってもおちついて対処できます",
            "emoji": "😌",
        },
        "learning": {
            "title": "まなぶ意欲",
            "description": "新しいことを覚えようとします",
            "emoji": "📚",
        },
    }

    challenge_map = {
        "focus": {
            "title": "集中の練習",
            "description": "同じ作業を続けることを練習中",
            "emoji": "🔁",
        },
        "communication": {
            "title": "はなす練習",
            "description": "わからないとき伝える練習中",
            "emoji": "👋",
        },
        "endurance": {
            "title": "体力づくり",
            "description": "体を動かす習慣をつけています",
            "emoji": "💪",
        },
        "accuracy": {
            "title": "ていねいさの練習",
            "description": "正確に作業する練習中",
            "emoji": "🔍",
        },
        "emotion_control": {
            "title": "きもちのコントロール",
            "description": "おちつく方法を練習中",
            "emoji": "😌",
        },
        "learning": {
            "title": "チャレンジする練習",
            "description": "新しいことに少しずつ挑戦中",
            "emoji": "📚",
        },
    }

    strengths = [
        {**strength_map[t], "trait": t}
        for t, _ in sorted_traits[:2]
        if t in strength_map
    ]
    challenges = [
        {**challenge_map[t], "trait": t}
        for t, _ in sorted_traits[-2:]
        if t in challenge_map
    ]

    job_type_messages = {
        "agriculture": "農業・園芸系の仕事が向いていそうです！植物を育てたり、外で体を使う仕事が向いています。",
        "manufacturing": "製造・組み立て系の仕事が向いていそうです！丁寧に同じ作業を続けることが得意なあなたにぴったりです。",
        "cleaning": "清掃・環境整備の仕事が向いていそうです！きれいにすることが得意なあなたにぴったりです。",
        "food_processing": "食品加工系の仕事が向いていそうです！丁寧で正確な作業が得意なあなたにぴったりです。",
        "service": "接客・販売補助系の仕事が向いていそうです！人と関わることが得意なあなたにぴったりです。",
    }

    default_message = "あなたには素晴らしい可能性があります。一歩ずつ進んでいきましょう！"

    return {
        "strengths": strengths,
        "challenges": challenges,
        "job_type": job_type,
        "summary": job_type_messages.get(job_type, default_message),
        "trait_scores": trait_scores,
    }
