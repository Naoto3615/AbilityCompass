import json
from django.conf import settings


def resolve_data(obj, mode):
    """データをテキストモードに応じて変換。
    
    - dict に 'kanji'/'hiragana' キーがある場合: mode に対応するテキストを返す
    - 平文文字列の場合: hiragana モードなら pykakasi で自動変換
    - list/dict のネスト: 再帰処理
    """
    if isinstance(obj, dict):
        if 'kanji' in obj and 'hiragana' in obj:
            return obj.get(mode, obj.get('kanji', ''))
        return {k: resolve_data(v, mode) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_data(item, mode) for item in obj]
    elif isinstance(obj, str) and mode == 'hiragana':
        try:
            from diagnosis.templatetags.text_mode import to_hiragana
            return to_hiragana(obj)
        except Exception:
            return obj
    return obj


# ─── ロードマップ 3ステップ定義 ─────────────────────────────────────────────

STEP_DEFINITIONS = {
    1: {
        "name": "ステップ 1",
        "theme": "生活習慣・基本スキル",
        "emoji": "🌱",
        "color": "green",
        "description": "働く前に、まず毎日の生活を整えよう",
    },
    2: {
        "name": "ステップ 2",
        "theme": "作業スキル",
        "emoji": "🔧",
        "color": "blue",
        "description": "指示どおりに動けるよう、くりかえし練習しよう",
    },
    3: {
        "name": "ステップ 3",
        "theme": "就労準備",
        "emoji": "🚀",
        "color": "orange",
        "description": "実際の仕事に近い体験をしてみよう",
    },
}

# ─── 仕事タイプ別ロードマップ ──────────────────────────────────────────────
ROADMAP_DATA = {

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "agriculture": {
        1: {
            "tasks": [
                {
                    "category": "生活習慣",
                    "content": "毎日決まった時間に起きる",
                    "daily_action": "今日は朝、時間どおりに起きてみよう ⏰",
                },
                {
                    "category": "あいさつ",
                    "content": "「おはようございます」と言えるようにする",
                    "daily_action": "家の人に「おはようございます」と言ってみよう 👋",
                },
                {
                    "category": "体力づくり",
                    "content": "毎日少し外で体を動かす",
                    "daily_action": "今日は10分外を歩いてみよう 🚶",
                },
                {
                    "category": "基礎スキル",
                    "content": "自分の体調を人に伝える",
                    "daily_action": "今日の体の調子を人に話してみよう 💬",
                },
            ],
            "message": "まず毎日の生活を整えることが第一歩！",
        },
        2: {
            "tasks": [
                {
                    "category": "作業練習",
                    "content": "丁寧にものを扱う練習をする",
                    "daily_action": "今日は飲み物・食べ物を丁寧に扱ってみよう 🌿",
                },
                {
                    "category": "指示理解",
                    "content": "「最後まで聞いてから動く」を練習する",
                    "daily_action": "人が話している間、最後まで聞いてみよう 👂",
                },
                {
                    "category": "くりかえし作業",
                    "content": "同じ作業を30分続ける練習",
                    "daily_action": "お茶碗洗いや掃除を30分続けてみよう 🧹",
                },
                {
                    "category": "報告",
                    "content": "作業が終わったら「できました」と言う",
                    "daily_action": "今日何かが終わったら「できました！」と言ってみよう ✅",
                },
            ],
            "message": "くりかえし練習すると体が覚えてくるよ！",
        },
        3: {
            "tasks": [
                {
                    "category": "体験学習",
                    "content": "農業・園芸の体験に参加する",
                    "daily_action": "近くの農園や園芸教室を調べてみよう 🌱",
                },
                {
                    "category": "職場体験",
                    "content": "福祉的就労やジョブコーチとの連携を調べる",
                    "daily_action": "支援員さんに「職場体験したい」と伝えてみよう 🤝",
                },
                {
                    "category": "自己PR",
                    "content": "自分の強みを短く言えるようにする",
                    "daily_action": "「私は○○が得意です」と鏡に向かって言ってみよう 💪",
                },
            ],
            "message": "実際の仕事に近い体験をしてみよう！",
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "manufacturing": {
        1: {
            "tasks": [
                {
                    "category": "生活習慣",
                    "content": "時刻を守る習慣をつける",
                    "daily_action": "今日は約束の時間にごはんを食べてみよう ⏰",
                },
                {
                    "category": "あいさつ",
                    "content": "「おはようございます」「お先に失礼します」を練習",
                    "daily_action": "今日家を出るとき・戻るときあいさつしてみよう 👋",
                },
                {
                    "category": "集中力",
                    "content": "一つのことに集中する時間を伸ばす",
                    "daily_action": "今日は20分何か一つだけに集中してみよう 🎯",
                },
                {
                    "category": "基礎スキル",
                    "content": "手順を守って作業する練習",
                    "daily_action": "今日の片付けを順番どおりにやってみよう 📋",
                },
            ],
            "message": "手順を守ることが製造の仕事の基本だよ！",
        },
        2: {
            "tasks": [
                {
                    "category": "作業練習",
                    "content": "細かいものを丁寧に扱う練習",
                    "daily_action": "細かいパズルやレゴを丁寧に組み立ててみよう 🔧",
                },
                {
                    "category": "品質確認",
                    "content": "「できた！」のあともう一度確かめる習慣",
                    "daily_action": "今日何かをしたあと「間違いないかな？」と見直してみよう 🔍",
                },
                {
                    "category": "くりかえし作業",
                    "content": "同じ手順を何度も練習する",
                    "daily_action": "紙を折る・塗り絵を塗るなどくりかえす作業をやってみよう ♻️",
                },
                {
                    "category": "報告",
                    "content": "ミスをしたとき、すぐに伝える練習",
                    "daily_action": "今日失敗したことを正直に人に伝えてみよう 💬",
                },
            ],
            "message": "丁寧さと確認が製造の仕事の最大の武器！",
        },
        3: {
            "tasks": [
                {
                    "category": "体験学習",
                    "content": "製造系の福祉的就労や工場見学に参加する",
                    "daily_action": "支援センターに「工場見学したい」と相談してみよう 🏭",
                },
                {
                    "category": "職場体験",
                    "content": "ライン作業の体験をする",
                    "daily_action": "封筒にチラシを入れるなどくりかえし作業をやってみよう 📦",
                },
                {
                    "category": "自己PR",
                    "content": "「丁寧にできます」を自信を持って言えるようにする",
                    "daily_action": "「私は丁寧に作業します」と鏡に言ってみよう 💪",
                },
            ],
            "message": "実際の工場に近い体験をしよう！",
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "cleaning": {
        1: {
            "tasks": [
                {
                    "category": "生活習慣",
                    "content": "自分の部屋を毎日片付ける",
                    "daily_action": "今日は自分の部屋を5分片付けてみよう 🧹",
                },
                {
                    "category": "あいさつ",
                    "content": "すれ違う人に「こんにちは」と言える",
                    "daily_action": "今日人に会ったら「こんにちは」と言ってみよう 👋",
                },
                {
                    "category": "体力づくり",
                    "content": "体を動かす習慣をつける",
                    "daily_action": "今日は家の周りを10分歩いてみよう 🚶",
                },
                {
                    "category": "基礎スキル",
                    "content": "掃除道具の使い方を覚える",
                    "daily_action": "ほうき・雑巾の使い方を練習してみよう 🧽",
                },
            ],
            "message": "きれいにする仕事の基本は自分の周りをきれいにすること！",
        },
        2: {
            "tasks": [
                {
                    "category": "作業練習",
                    "content": "掃除の手順を覚えてくりかえす",
                    "daily_action": "トイレや玄関を順番どおりに掃除してみよう 🚿",
                },
                {
                    "category": "確認",
                    "content": "掃除のあと「見残しがないか」確認する",
                    "daily_action": "今日の掃除のあと汚れが残っていないか見てみよう 🔍",
                },
                {
                    "category": "くりかえし作業",
                    "content": "同じ掃除を毎日同じ手順でおこなう",
                    "daily_action": "今日も昨日と同じ手順で掃除してみよう ♻️",
                },
                {
                    "category": "報告",
                    "content": "掃除が終わったら「できました」と点検する",
                    "daily_action": "掃除が終わったら「終わりました！」と言ってみよう ✅",
                },
            ],
            "message": "毎日同じ手順で掃除すると上手になるよ！",
        },
        3: {
            "tasks": [
                {
                    "category": "体験学習",
                    "content": "清掃系福祉的就労の体験",
                    "daily_action": "支援センターに「清掃作業をやってみたい」と伝えよう 🧹",
                },
                {
                    "category": "職場体験",
                    "content": "施設の掃除を手伝う経験をする",
                    "daily_action": "家でみんなが使う場所を一生懸命掃除してみよう 🏢",
                },
                {
                    "category": "自己PR",
                    "content": "「きれいにする仕事が好きです」と言えるようにする",
                    "daily_action": "「私は掃除が好きです」と人に話してみよう 😊",
                },
            ],
            "message": "実際の環境整備の仕事を体験しよう！",
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "food_processing": {
        1: {
            "tasks": [
                {
                    "category": "生活習慣",
                    "content": "毎日決まった時間に食事をとる",
                    "daily_action": "今日は決まった時間にごはんを食べてみよう 🍚",
                },
                {
                    "category": "衛生習慣",
                    "content": "手洗いを丁寧におこなう",
                    "daily_action": "今日は20秒かけて丁寧に手を洗おう 🧼",
                },
                {
                    "category": "集中力",
                    "content": "丁寧にものを扱う習慣をつける",
                    "daily_action": "今日は食べものを丁寧に扱ってみよう 🍱",
                },
                {
                    "category": "基礎スキル",
                    "content": "順番を守って作業する",
                    "daily_action": "料理を手伝うとき決まった手順でやってみよう 👩‍🍳",
                },
            ],
            "message": "食べものを扱う仕事は清潔さが一番大事！",
        },
        2: {
            "tasks": [
                {
                    "category": "作業練習",
                    "content": "食べものをきれいに並べる練習",
                    "daily_action": "今日はお菓子や食べものをきれいに並べてみよう 📦",
                },
                {
                    "category": "品質確認",
                    "content": "分量を正しく量る練習",
                    "daily_action": "料理でスプーンを使ってきちんと量ってみよう ⚖️",
                },
                {
                    "category": "くりかえし作業",
                    "content": "同じ包装・詰める作業をくりかえす",
                    "daily_action": "お菓子を袋に入れる練習をやってみよう 🎁",
                },
                {
                    "category": "報告",
                    "content": "異常があったとき、すぐ伝える",
                    "daily_action": "何か変だと思ったらすぐ人に言う練習をしよう 💬",
                },
            ],
            "message": "丁寧さと規制を守ることが食品の仕事の要！",
        },
        3: {
            "tasks": [
                {
                    "category": "体験学習",
                    "content": "食品加工の福祉的就労を体験する",
                    "daily_action": "支援センターに「食品の仕事をやってみたい」と言おう 🍱",
                },
                {
                    "category": "職場体験",
                    "content": "お弁当や惣菜を作る経験をする",
                    "daily_action": "家で簡単なお弁当を自分で作ってみよう 🍙",
                },
                {
                    "category": "自己PR",
                    "content": "「丁寧できれい好きです」を言えるようにする",
                    "daily_action": "「私は丁寧に作業できます」と練習しよう 💪",
                },
            ],
            "message": "食品加工の仕事を体験して向いているか確かめよう！",
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "service": {
        1: {
            "tasks": [
                {
                    "category": "あいさつ",
                    "content": "「いらっしゃいませ」「ありがとうございます」を練習",
                    "daily_action": "今日家で「いらっしゃいませ」と高い声で言ってみよう 😊",
                },
                {
                    "category": "コミュニケーション",
                    "content": "人の話を最後まで聞く練習",
                    "daily_action": "今日誰かが話しているとき最後まで聞いてみよう 👂",
                },
                {
                    "category": "生活習慣",
                    "content": "見た目をきちんと整える習慣をつける",
                    "daily_action": "今日は髪をとかして服をきれいに着てみよう 👔",
                },
                {
                    "category": "基礎スキル",
                    "content": "「すみません」「ありがとう」を自然に言えるようにする",
                    "daily_action": "今日は3回「ありがとう」を使ってみよう 🙏",
                },
            ],
            "message": "笑顔とあいさつが接客の仕事の一番の武器！",
        },
        2: {
            "tasks": [
                {
                    "category": "接客練習",
                    "content": "丁寧な言葉を使って答える練習",
                    "daily_action": "家で「いらっしゃいませ、何かお手伝いしますか？」と練習しよう 🛒",
                },
                {
                    "category": "商品陳列",
                    "content": "ものをきれいに並べる練習",
                    "daily_action": "今日は本棚や冷蔵庫をきれいに並べ直してみよう 📦",
                },
                {
                    "category": "気づく力",
                    "content": "「人に気づいたら声をかける」練習",
                    "daily_action": "困っている人に気づいたら「何かお手伝いしましょうか？」と言ってみよう 💬",
                },
                {
                    "category": "報告",
                    "content": "わからないとき「教えてください」と言えるようにする",
                    "daily_action": "今日わからないことを「教えてください」と言ってみよう 🙋",
                },
            ],
            "message": "人にやさしく声をかけることが接客の仕事の鍵！",
        },
        3: {
            "tasks": [
                {
                    "category": "体験学習",
                    "content": "接客・販売補助の福祉的就労を体験する",
                    "daily_action": "支援センターに「お店の仕事を体験したい」と伝えよう 🛒",
                },
                {
                    "category": "職場体験",
                    "content": "ショッピングモールやスーパーで仕事を見る",
                    "daily_action": "スーパーで店員さんの仕事をじっくり見てみよう 🏪",
                },
                {
                    "category": "自己PR",
                    "content": "「笑顔で働けます」を自信を持って言えるようにする",
                    "daily_action": "鏡に向かって笑顔で「よろしくお願いします！」と言ってみよう 😊",
                },
            ],
            "message": "笑顔で働けるあなたがお店の大切な力になるよ！",
        },
    },
}


def get_step_definitions():
    return STEP_DEFINITIONS


def get_job_roadmap(job_type: str) -> dict:
    """仕事タイプのロードマップを返す（AI or フォールバック）"""
    try:
        return _generate_with_ai(job_type)
    except Exception:
        return _fallback_roadmap(job_type)


def _generate_with_ai(job_type: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    job_names = {
        "agriculture": "農業・園芸系",
        "manufacturing": "製造・組み立て系",
        "cleaning": "清掃・環境整備系",
        "food_processing": "食品加工系",
        "service": "接客・販売補助系",
    }
    job_name = job_names.get(job_type, job_type)

    prompt = f"""あなたは軽度知的障害のある大人の就労支援の専門家です。
「{job_name}」を目指す方への就労準備ロードマップを3ステップで作成してください。
文章はひらがな多用・やさしい日本語でお願いします。

以下のJSON形式で返してください：
{{
  "step1": {{
    "tasks": [
      {{"category": "カテゴリ名", "content": "タスク内容（30文字以内）", "daily_action": "今日できる行動（40文字以内）"}},
      ...（4つ）
    ],
    "message": "励ましのメッセージ（50文字以内）"
  }},
  "step2": {{
    "tasks": [...（4つ）],
    "message": "..."
  }},
  "step3": {{
    "tasks": [...（3つ）],
    "message": "..."
  }}
}}

必ずJSON形式のみ返してください。"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def _fallback_roadmap(job_type: str) -> dict:
    data = ROADMAP_DATA.get(job_type, ROADMAP_DATA["manufacturing"])
    result = {}
    for step_num in [1, 2, 3]:
        step_data = data.get(step_num, {})
        result[f"step{step_num}"] = {
            "tasks": step_data.get("tasks", []),
            "message": step_data.get("message", "一歩一歩頑張ろう！"),
        }
    return result


def get_supporter_advice(user, daily_records):
    """支援者向けAIアドバイス（フォールバックあり）"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        records_text = ""
        for r in daily_records[:7]:
            records_text += f"- {r.date}: きもち{r.get_emotion_label()}, できたこと「{r.did_well[:30] if r.did_well else '（なし）'}」\n"

        prompt = f"""就労支援の支援者として、以下の利用者の1週間の記録を見てアドバイスをください。
やさしい言葉で、支援者に向けた具体的なアドバイスを2〜3文で。

記録:
{records_text}

アドバイス:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()

    except Exception:
        if not daily_records:
            return "まだ記録がありません。利用者に記録をつけるよう声かけしてみましょう。"

        latest = daily_records[-1]
        if latest.emotion_stamp >= 4:
            return "最近きもちが安定しているようです。この調子を応援しつつ、次のステップへの声かけをしてみましょう。"
        elif latest.emotion_stamp <= 2:
            return "最近つらそうな日が続いています。ゆっくり話を聞く時間をとってみましょう。焦らず寄り添うことが大切です。"
        else:
            return "記録が続いています！毎日記録できていることを褒めてあげましょう。小さな成功体験が積み重なります。"
