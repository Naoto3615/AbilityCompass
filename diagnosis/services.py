import json
from django.conf import settings

DIAGNOSIS_QUESTIONS = [
    {
        "id": "q1",
        "category": "focus",
        "text": "好きなことや気になることに対して、時間を忘れて集中することがある",
        "emoji": "🔍",
    },
    {
        "id": "q2",
        "category": "pattern",
        "text": "数字・図形・パターンを見ると面白いと感じる",
        "emoji": "🔢",
    },
    {
        "id": "q3",
        "category": "creative",
        "text": "頭の中でイメージや絵を思い浮かべるのが得意だ",
        "emoji": "🎨",
    },
    {
        "id": "q4",
        "category": "movement",
        "text": "体を動かすことや手を使って何かを作ることが好きだ",
        "emoji": "🏃",
    },
    {
        "id": "q5",
        "category": "music",
        "text": "音楽を聴いたり、リズムや音の変化に気づくことが多い",
        "emoji": "🎵",
    },
    {
        "id": "q6",
        "category": "nature",
        "text": "動物や植物・自然現象に強い興味を持っている",
        "emoji": "🌿",
    },
    {
        "id": "q7",
        "category": "empathy",
        "text": "他の人や動物の気持ちを察したり、共感することが多い",
        "emoji": "💗",
    },
    {
        "id": "q8",
        "category": "rule",
        "text": "ルールや手順を守ることに強いこだわりを感じる",
        "emoji": "📋",
    },
    {
        "id": "q9",
        "category": "detail",
        "text": "細かいところや他の人が見落とすようなことに気づく",
        "emoji": "🔎",
    },
    {
        "id": "q10",
        "category": "story",
        "text": "物語を読んだり話を作ったりするのが好きだ",
        "emoji": "📖",
    },
    {
        "id": "q11",
        "category": "logic",
        "text": "「なぜ？」「どうして？」と理由を考えるのが好きだ",
        "emoji": "🤔",
    },
    {
        "id": "q12",
        "category": "social",
        "text": "みんなで協力して何かを達成するよりも、一人で取り組む方が好きだ",
        "emoji": "🧩",
    },
    {
        "id": "q13",
        "category": "memory",
        "text": "好きなテーマについての知識や情報をたくさん覚えている",
        "emoji": "🧠",
    },
    {
        "id": "q14",
        "category": "system",
        "text": "物事を整理したり、順番を決めたりするのが好きだ",
        "emoji": "📊",
    },
    {
        "id": "q15",
        "category": "visual",
        "text": "説明を読むより、図や絵で見た方が理解しやすい",
        "emoji": "🖼️",
    },
]

SCORE_LABELS = {
    1: "まったくあてはまらない",
    2: "あまりあてはまらない",
    3: "どちらともいえない",
    4: "ややあてはまる",
    5: "よくあてはまる",
}

CAREER_LIST = [
    {"key": "programmer", "name": "プログラマー・エンジニア", "emoji": "💻"},
    {"key": "designer", "name": "デザイナー・アーティスト", "emoji": "🎨"},
    {"key": "musician", "name": "音楽家・作曲家", "emoji": "🎼"},
    {"key": "scientist", "name": "科学者・研究者", "emoji": "🔬"},
    {"key": "writer", "name": "作家・ライター", "emoji": "✍️"},
    {"key": "mathematician", "name": "数学者・データサイエンティスト", "emoji": "📐"},
    {"key": "game_creator", "name": "ゲームクリエイター", "emoji": "🎮"},
    {"key": "chef", "name": "シェフ・料理研究家", "emoji": "👨‍🍳"},
    {"key": "animal_care", "name": "動物の専門家", "emoji": "🐾"},
    {"key": "architect", "name": "建築家・空間デザイナー", "emoji": "🏛️"},
    {"key": "teacher", "name": "教師・支援員", "emoji": "📚"},
    {"key": "athlete", "name": "スポーツ選手・コーチ", "emoji": "⚽"},
    {"key": "photographer", "name": "写真家・映像作家", "emoji": "📷"},
    {"key": "entrepreneur", "name": "起業家・経営者", "emoji": "🚀"},
    {"key": "doctor", "name": "医師・医療専門家", "emoji": "🩺"},
]


def get_questions():
    return DIAGNOSIS_QUESTIONS


def get_career_list():
    return CAREER_LIST


def analyze_with_ai(answers: dict) -> dict:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        questions_text = "\n".join(
            f"Q{i+1}. {q['text']}（スコア: {answers.get(q['id'], 3)}/5）"
            for i, q in enumerate(DIAGNOSIS_QUESTIONS)
        )

        career_names = "、".join(f"{c['name']}" for c in CAREER_LIST)

        prompt = f"""あなたは発達障害を持つ子供たちの強みを発見する専門家です。
以下は子供（または保護者）が答えた自己評価アンケートの結果です（1=あてはまらない、5=よくあてはまる）。

{questions_text}

この結果を分析して、以下のJSON形式で返してください：

{{
  "strengths": [
    {{"title": "強みの名前（10文字以内）", "description": "強みの説明（50文字以内）", "emoji": "絵文字1つ"}},
    {{"title": "強みの名前", "description": "説明", "emoji": "絵文字"}},
    {{"title": "強みの名前", "description": "説明", "emoji": "絵文字"}}
  ],
  "careers": [
    {{"key": "職業キー", "name": "職業名", "emoji": "絵文字", "reason": "この職業が向いている理由（60文字以内）", "match_score": 90}},
    {{"key": "職業キー", "name": "職業名", "emoji": "絵文字", "reason": "理由", "match_score": 85}},
    {{"key": "職業キー", "name": "職業名", "emoji": "絵文字", "reason": "理由", "match_score": 80}}
  ],
  "summary": "この子の特性と可能性についての温かいメッセージ（100文字以内、ポジティブな表現で）"
}}

職業キーは以下から選択してください：{', '.join(c['key'] for c in CAREER_LIST)}
必ずJSON形式のみを返してください。説明文は不要です。"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        return _fallback_analysis(answers)


def _fallback_analysis(answers: dict) -> dict:
    """OpenAI APIが使えない場合のフォールバック分析"""
    category_scores = {}
    for q in DIAGNOSIS_QUESTIONS:
        score = int(answers.get(q["id"], 3))
        cat = q["category"]
        category_scores[cat] = category_scores.get(cat, 0) + score

    top_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)

    strength_map = {
        "focus": {"title": "深い集中力", "description": "好きなことに徹底的に集中できる力", "emoji": "🔍"},
        "pattern": {"title": "パターン認識", "description": "規則性や構造を見抜く鋭い目", "emoji": "🔢"},
        "creative": {"title": "豊かな想像力", "description": "頭の中でイメージを自在に描く力", "emoji": "🎨"},
        "movement": {"title": "身体的な表現力", "description": "体や手を使って表現・制作する力", "emoji": "🏃"},
        "music": {"title": "音楽的感性", "description": "音やリズムへの鋭い感受性", "emoji": "🎵"},
        "nature": {"title": "自然への好奇心", "description": "生き物や自然現象への深い興味", "emoji": "🌿"},
        "empathy": {"title": "高い共感力", "description": "他者の感情を敏感に感じ取る力", "emoji": "💗"},
        "rule": {"title": "規律と一貫性", "description": "ルールを守り、一貫した行動をとる力", "emoji": "📋"},
        "detail": {"title": "細部への注意力", "description": "見落としがちな細かい部分に気づく力", "emoji": "🔎"},
        "story": {"title": "物語を作る力", "description": "豊かな語彙で物語を紡ぎ出す力", "emoji": "📖"},
        "logic": {"title": "論理的思考力", "description": "物事の理由や仕組みを追究する力", "emoji": "🤔"},
        "social": {"title": "独立した集中力", "description": "自分のペースで深く取り組む力", "emoji": "🧩"},
        "memory": {"title": "専門的な記憶力", "description": "興味あるテーマの知識を蓄積する力", "emoji": "🧠"},
        "system": {"title": "整理・体系化の力", "description": "情報を整理して構造化する力", "emoji": "📊"},
        "visual": {"title": "視覚的思考力", "description": "図や絵で物事を理解・表現する力", "emoji": "🖼️"},
    }

    strengths = [strength_map[cat] for cat, _ in top_categories[:3] if cat in strength_map]

    career_map = {
        "focus": "programmer",
        "pattern": "mathematician",
        "creative": "designer",
        "movement": "athlete",
        "music": "musician",
        "nature": "scientist",
        "empathy": "doctor",
        "rule": "programmer",
        "detail": "photographer",
        "story": "writer",
        "logic": "scientist",
        "social": "researcher",
        "memory": "scientist",
        "system": "architect",
        "visual": "designer",
    }

    suggested_career_keys = []
    for cat, _ in top_categories[:3]:
        key = career_map.get(cat)
        if key and key not in suggested_career_keys:
            suggested_career_keys.append(key)

    careers = []
    for c in CAREER_LIST:
        if c["key"] in suggested_career_keys:
            careers.append({
                "key": c["key"],
                "name": c["name"],
                "emoji": c["emoji"],
                "reason": "あなたの特性・強みと高い親和性があります",
                "match_score": 85,
            })

    return {
        "strengths": strengths[:3],
        "careers": careers[:3],
        "summary": "あなたには素晴らしい個性と可能性があります。自分の強みを信じて、一歩ずつ進んでいきましょう！",
    }
