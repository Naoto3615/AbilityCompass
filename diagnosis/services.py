import json
from django.conf import settings

# ─── 診断質問（漢字・ひらがな両対応） ────────────────────────────────────────
DIAGNOSIS_QUESTIONS = [
    # 集中力（3問）
    {
        "id": "q1",
        "category": "focus",
        "text": {"kanji": "同じ作業をずっとくりかえすことができる", "hiragana": "おなじさぎょうを　ずっと　くりかえすことが　できる"},
        "emoji": "🔁",
    },
    {
        "id": "q2",
        "category": "focus",
        "text": {"kanji": "好きな作業は時間を忘れて一生懸命できる", "hiragana": "すきなさぎょうは　じかんを　わすれて　いっしょうけんめい　できる"},
        "emoji": "⏰",
    },
    {
        "id": "q3",
        "category": "focus",
        "text": {"kanji": "最後まであきらめずに作業を続けられる", "hiragana": "さいごまで　あきらめずに　さぎょうを　つづけられる"},
        "emoji": "🎯",
    },
    # コミュニケーション力（2問）
    {
        "id": "q4",
        "category": "communication",
        "text": {"kanji": "わからないとき「わかりません」と言える", "hiragana": "わからないとき　「わかりません」と　いえる"},
        "emoji": "🙋",
    },
    {
        "id": "q5",
        "category": "communication",
        "text": {"kanji": "「おはようございます」「ありがとうございます」のあいさつができる", "hiragana": "「おはようございます」「ありがとうございます」の　あいさつが　できる"},
        "emoji": "👋",
    },
    # 体力・持続力（2問）
    {
        "id": "q6",
        "category": "endurance",
        "text": {"kanji": "体を動かす仕事が好き", "hiragana": "からだを　うごかす　しごとが　すき"},
        "emoji": "💪",
    },
    {
        "id": "q7",
        "category": "endurance",
        "text": {"kanji": "1日中立って仕事をしても疲れにくい", "hiragana": "1日じゅう　たって　しごとを　しても　つかれにくい"},
        "emoji": "🏃",
    },
    # 几帳面さ・正確性（2問）
    {
        "id": "q8",
        "category": "accuracy",
        "text": {"kanji": "ものをきれいに並べたり整理することが好き", "hiragana": "ものを　きれいに　ならべたり　せいりすることが　すき"},
        "emoji": "📦",
    },
    {
        "id": "q9",
        "category": "accuracy",
        "text": {"kanji": "まちがいを見つけることや丁寧にやることが得意", "hiragana": "まちがいを　みつけること　や　ていねいに　やることが　とくい"},
        "emoji": "🔍",
    },
    # 感情コントロール（2問）
    {
        "id": "q10",
        "category": "emotion_control",
        "text": {"kanji": "うまくできないとき、落ち着いてやり直せる", "hiragana": "うまく　できないとき　おちついて　やりなおせる"},
        "emoji": "😌",
    },
    {
        "id": "q11",
        "category": "emotion_control",
        "text": {"kanji": "予定が変わっても、パニックになりにくい", "hiragana": "よていが　かわっても　パニックに　なりにくい"},
        "emoji": "🧘",
    },
    # 学習意欲・変化への適応（2問）
    {
        "id": "q12",
        "category": "learning",
        "text": {"kanji": "新しいことを教えてもらうのが好き", "hiragana": "あたらしいことを　おしえてもらうのが　すき"},
        "emoji": "📚",
    },
    {
        "id": "q13",
        "category": "learning",
        "text": {"kanji": "できないことができるようになると嬉しい", "hiragana": "できないことが　できるようになると　うれしい"},
        "emoji": "⭐",
    },
]

SCORE_LABELS = {
    1: {"kanji": "全然あてはまらない", "hiragana": "ぜんぜん　あてはまらない"},
    2: {"kanji": "あまりあてはまらない", "hiragana": "あまり　あてはまらない"},
    3: {"kanji": "どちらとも言えない", "hiragana": "どちらとも　いえない"},
    4: {"kanji": "少しあてはまる", "hiragana": "すこし　あてはまる"},
    5: {"kanji": "とてもあてはまる", "hiragana": "とても　あてはまる"},
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
        "name": {"kanji": "農業・園芸系", "hiragana": "のうぎょう・えんげいけい"},
        "emoji": "🌱",
        "description": {"kanji": "いちごや野菜を育てたり、植物の世話をする仕事", "hiragana": "いちごや やさいを そだてたり、しょくぶつの せわを する しごと"},
        "color": "green",
    },
    {
        "key": "manufacturing",
        "name": {"kanji": "製造・組み立て系", "hiragana": "せいぞう・くみたてけい"},
        "emoji": "🔧",
        "description": {"kanji": "部品を組み立てたり、決まった手順で作業する仕事", "hiragana": "ぶひんを くみたてたり、きまった てじゅんで さぎょうする しごと"},
        "color": "blue",
    },
    {
        "key": "cleaning",
        "name": {"kanji": "清掃・環境整備系", "hiragana": "せいそう・かんきょうせいびけい"},
        "emoji": "🧹",
        "description": {"kanji": "建物や施設をきれいに掃除・整理する仕事", "hiragana": "たてものや しせつを きれいに そうじ・せいりする しごと"},
        "color": "sky",
    },
    {
        "key": "food_processing",
        "name": {"kanji": "食品加工系", "hiragana": "しょくひんかこうけい"},
        "emoji": "🍱",
        "description": {"kanji": "食べ物を作ったり、袋に入れたりする仕事", "hiragana": "たべものを つくったり、ふくろに いれたりする しごと"},
        "color": "orange",
    },
    {
        "key": "service",
        "name": {"kanji": "接客・販売補助系", "hiragana": "せっきゃく・はんばいほじょけい"},
        "emoji": "🛒",
        "description": {"kanji": "お店でお客さんのお手伝いや商品を並べる仕事", "hiragana": "おみせで おきゃくさんの おてつだいや しょうひんを ならべる しごと"},
        "color": "pink",
    },
]

# ─── 特性ラベル ──────────────────────────────────────────────────────────────
TRAIT_LABELS = {
    "focus": {
        "name": {"kanji": "集中力", "hiragana": "しゅうちゅうりょく"},
        "emoji": "🔁",
        "desc": {"kanji": "同じ作業をずっと続ける力", "hiragana": "おなじ さぎょうを ずっと つづける ちから"},
    },
    "communication": {
        "name": {"kanji": "コミュニケーション力", "hiragana": "コミュニケーションりょく"},
        "emoji": "👋",
        "desc": {"kanji": "指示を聞いたり報告する力", "hiragana": "しじを きいたり ほうこくする ちから"},
    },
    "endurance": {
        "name": {"kanji": "体力・持続力", "hiragana": "たいりょく・じぞくりょく"},
        "emoji": "💪",
        "desc": {"kanji": "体を使う仕事を続ける力", "hiragana": "からだを つかう しごとを つづける ちから"},
    },
    "accuracy": {
        "name": {"kanji": "几帳面さ・正確性", "hiragana": "きちょうめんさ・せいかくせい"},
        "emoji": "🔍",
        "desc": {"kanji": "ていねいに正確に作業する力", "hiragana": "ていねいに せいかくに さぎょうする ちから"},
    },
    "emotion_control": {
        "name": {"kanji": "感情コントロール", "hiragana": "かんじょうコントロール"},
        "emoji": "😌",
        "desc": {"kanji": "落ち着いて対処する力", "hiragana": "おちついて たいしょする ちから"},
    },
    "learning": {
        "name": {"kanji": "学習意欲・適応力", "hiragana": "がくしゅういよく・てきおうりょく"},
        "emoji": "📚",
        "desc": {"kanji": "新しいことを覚えようとする力", "hiragana": "あたらしいことを おぼえようとする ちから"},
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
            f"Q{i+1}. {q['text']['hiragana'] if isinstance(q['text'], dict) else q['text']}（スコア: {answers.get(q['id'], 3)}/5）"
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
            "title": {"kanji": "集中する力", "hiragana": "しゅうちゅうする ちから"},
            "description": {"kanji": "同じ作業をずっと続けられます", "hiragana": "おなじ さぎょうを ずっと つづけられます"},
            "emoji": "🔁",
        },
        "communication": {
            "title": {"kanji": "コミュニケーション力", "hiragana": "コミュニケーションりょく"},
            "description": {"kanji": "あいさつや報告ができます", "hiragana": "あいさつや ほうこくが できます"},
            "emoji": "👋",
        },
        "endurance": {
            "title": {"kanji": "体力・続ける力", "hiragana": "たいりょく・つづける ちから"},
            "description": {"kanji": "体を使う仕事が得意です", "hiragana": "からだを つかう しごとが とくいです"},
            "emoji": "💪",
        },
        "accuracy": {
            "title": {"kanji": "ていねいさ", "hiragana": "ていねいさ"},
            "description": {"kanji": "正確に作業できます", "hiragana": "せいかくに さぎょうできます"},
            "emoji": "🔍",
        },
        "emotion_control": {
            "title": {"kanji": "落ち着く力", "hiragana": "おちつく ちから"},
            "description": {"kanji": "困ってもおちついて対処できます", "hiragana": "こまっても おちついて たいしょできます"},
            "emoji": "😌",
        },
        "learning": {
            "title": {"kanji": "まなぶ意欲", "hiragana": "まなぶ いよく"},
            "description": {"kanji": "新しいことを覚えようとします", "hiragana": "あたらしいことを おぼえようとします"},
            "emoji": "📚",
        },
    }

    challenge_map = {
        "focus": {
            "title": {"kanji": "集中の練習", "hiragana": "しゅうちゅうの れんしゅう"},
            "description": {"kanji": "同じ作業を続けることを練習中", "hiragana": "おなじ さぎょうを つづけることを れんしゅうちゅう"},
            "emoji": "🔁",
        },
        "communication": {
            "title": {"kanji": "はなす練習", "hiragana": "はなす れんしゅう"},
            "description": {"kanji": "わからないとき伝える練習中", "hiragana": "わからないとき つたえる れんしゅうちゅう"},
            "emoji": "👋",
        },
        "endurance": {
            "title": {"kanji": "体力づくり", "hiragana": "たいりょくづくり"},
            "description": {"kanji": "体を動かす習慣をつけています", "hiragana": "からだを うごかす しゅうかんを つけています"},
            "emoji": "💪",
        },
        "accuracy": {
            "title": {"kanji": "ていねいさの練習", "hiragana": "ていねいさの れんしゅう"},
            "description": {"kanji": "正確に作業する練習中", "hiragana": "せいかくに さぎょうする れんしゅうちゅう"},
            "emoji": "🔍",
        },
        "emotion_control": {
            "title": {"kanji": "きもちのコントロール", "hiragana": "きもちの コントロール"},
            "description": {"kanji": "おちつく方法を練習中", "hiragana": "おちつく ほうほうを れんしゅうちゅう"},
            "emoji": "😌",
        },
        "learning": {
            "title": {"kanji": "チャレンジする練習", "hiragana": "チャレンジする れんしゅう"},
            "description": {"kanji": "新しいことに少しずつ挑戦中", "hiragana": "あたらしいことに すこしずつ ちょうせんちゅう"},
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
        "agriculture": {
            "kanji": "農業・園芸系の仕事が向いていそうです！植物を育てたり、外で体を使う仕事が向いています。",
            "hiragana": "のうぎょう・えんげいけいの しごとが むいていそうです！しょくぶつを そだてたり、そとで からだを つかう しごとが むいています。",
        },
        "manufacturing": {
            "kanji": "製造・組み立て系の仕事が向いていそうです！丁寧に同じ作業を続けることが得意なあなたにぴったりです。",
            "hiragana": "せいぞう・くみたてけいの しごとが むいていそうです！ていねいに おなじ さぎょうを つづけることが とくいな あなたに ぴったりです。",
        },
        "cleaning": {
            "kanji": "清掃・環境整備の仕事が向いていそうです！きれいにすることが得意なあなたにぴったりです。",
            "hiragana": "せいそう・かんきょうせいびの しごとが むいていそうです！きれいにすることが とくいな あなたに ぴったりです。",
        },
        "food_processing": {
            "kanji": "食品加工系の仕事が向いていそうです！丁寧で正確な作業が得意なあなたにぴったりです。",
            "hiragana": "しょくひんかこうけいの しごとが むいていそうです！ていねいで せいかくな さぎょうが とくいな あなたに ぴったりです。",
        },
        "service": {
            "kanji": "接客・販売補助系の仕事が向いていそうです！人と関わることが得意なあなたにぴったりです。",
            "hiragana": "せっきゃく・はんばいほじょけいの しごとが むいていそうです！ひとと かかわることが とくいな あなたに ぴったりです。",
        },
    }

    default_message = {
        "kanji": "あなたには素晴らしい可能性があります。一歩ずつ進んでいきましょう！",
        "hiragana": "あなたには すばらしい かのうせいが あります。いっぽずつ すすんでいきましょう！",
    }

    return {
        "strengths": strengths,
        "challenges": challenges,
        "job_type": job_type,
        "summary": job_type_messages.get(job_type, default_message),
        "trait_scores": trait_scores,
    }
