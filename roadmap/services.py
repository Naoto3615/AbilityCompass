import json
from django.conf import settings


def resolve_data(obj, mode):
    """辞書 {'kanji': ..., 'hiragana': ...} を mode に合わせて文字列に変換。ネストも再帰処理。"""
    if isinstance(obj, dict):
        if 'kanji' in obj and 'hiragana' in obj:
            return obj[mode]
        return {k: resolve_data(v, mode) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_data(item, mode) for item in obj]
    return obj


# ─── ロードマップ 3ステップ定義 ─────────────────────────────────────────────

STEP_DEFINITIONS = {
    1: {
        "name": "ステップ 1",
        "theme": {"kanji": "生活習慣・基本スキル", "hiragana": "せいかつしゅうかん・きほんすきる"},
        "emoji": "🌱",
        "color": "green",
        "description": {"kanji": "働く前に、まず毎日の生活を整えよう", "hiragana": "はたらく まえに、まず まいにちの せいかつを ととのえよう"},
    },
    2: {
        "name": "ステップ 2",
        "theme": {"kanji": "作業スキル", "hiragana": "さぎょうすきる"},
        "emoji": "🔧",
        "color": "blue",
        "description": {"kanji": "指示どおりに動けるよう、くりかえし練習しよう", "hiragana": "しじどおりに うごけるよう、くりかえし れんしゅうしよう"},
    },
    3: {
        "name": "ステップ 3",
        "theme": {"kanji": "就労準備", "hiragana": "しゅうろうじゅんび"},
        "emoji": "🚀",
        "color": "orange",
        "description": {"kanji": "実際の仕事に近い体験をしてみよう", "hiragana": "じっさいの しごとに ちかい たいけんを してみよう"},
    },
}

# ─── 仕事タイプ別ロードマップ ──────────────────────────────────────────────
ROADMAP_DATA = {

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "agriculture": {
        1: {
            "tasks": [
                {
                    "category": {"kanji": "生活習慣", "hiragana": "せいかつしゅうかん"},
                    "content": {"kanji": "毎日決まった時間に起きる", "hiragana": "まいにち　きまった　じかんに　おきる"},
                    "daily_action": {"kanji": "今日は朝、時間どおりに起きてみよう ⏰", "hiragana": "きょうは　あさ　じかんどおりに　おきてみよう ⏰"},
                },
                {
                    "category": {"kanji": "あいさつ", "hiragana": "あいさつ"},
                    "content": {"kanji": "「おはようございます」と言えるようにする", "hiragana": "「おはようございます」を　いえるようにする"},
                    "daily_action": {"kanji": "家の人に「おはようございます」と言ってみよう 👋", "hiragana": "いえの　ひとに　「おはようございます」を　いってみよう 👋"},
                },
                {
                    "category": {"kanji": "体力づくり", "hiragana": "たいりょくづくり"},
                    "content": {"kanji": "毎日少し外で体を動かす", "hiragana": "まいにち　すこし　そとで　からだを　うごかす"},
                    "daily_action": {"kanji": "今日は10分外を歩いてみよう 🚶", "hiragana": "きょうは　10ぷん　そとを　あるいてみよう 🚶"},
                },
                {
                    "category": {"kanji": "基礎スキル", "hiragana": "きそすきる"},
                    "content": {"kanji": "自分の体調を人に伝える", "hiragana": "じぶんの　ちょうしを　ひとに　つたえる"},
                    "daily_action": {"kanji": "今日の体の調子を人に話してみよう 💬", "hiragana": "きょうの　からだの　ちょうしを　ひとに　はなしてみよう 💬"},
                },
            ],
            "message": {"kanji": "まず毎日の生活を整えることが第一歩！", "hiragana": "まずは　まいにちの　せいかつを　ととのえることが　だいいっぽ！"},
        },
        2: {
            "tasks": [
                {
                    "category": {"kanji": "作業練習", "hiragana": "さぎょうれんしゅう"},
                    "content": {"kanji": "丁寧にものを扱う練習をする", "hiragana": "ていねいに　ものを　あつかう　れんしゅうをする"},
                    "daily_action": {"kanji": "今日は飲み物・食べ物を丁寧に扱ってみよう 🌿", "hiragana": "きょうは　のみもの・たべものを　ていねいに　あつかってみよう 🌿"},
                },
                {
                    "category": {"kanji": "指示理解", "hiragana": "しじりかい"},
                    "content": {"kanji": "「最後まで聞いてから動く」を練習する", "hiragana": "「さいごまで　きいてから　うごく」を　れんしゅうする"},
                    "daily_action": {"kanji": "人が話している間、最後まで聞いてみよう 👂", "hiragana": "ひとが　はなしているあいだ　さいごまで　きいてみよう 👂"},
                },
                {
                    "category": {"kanji": "くりかえし作業", "hiragana": "くりかえし さぎょう"},
                    "content": {"kanji": "同じ作業を30分続ける練習", "hiragana": "おなじ　さぎょうを　30ぷん　つづける　れんしゅう"},
                    "daily_action": {"kanji": "お茶碗洗いや掃除を30分続けてみよう 🧹", "hiragana": "おちゃわんあらいや　そうじを　30ぷん　つづけてみよう 🧹"},
                },
                {
                    "category": {"kanji": "報告", "hiragana": "ほうこく"},
                    "content": {"kanji": "作業が終わったら「できました」と言う", "hiragana": "さぎょうが　おわったら　「できました」と　いう"},
                    "daily_action": {"kanji": "今日何かが終わったら「できました！」と言ってみよう ✅", "hiragana": "きょう　なにかが　おわったら　「できました！」と　いってみよう ✅"},
                },
            ],
            "message": {"kanji": "くりかえし練習すると体が覚えてくるよ！", "hiragana": "くりかえし　れんしゅうすると　からだが　おぼえてくるよ！"},
        },
        3: {
            "tasks": [
                {
                    "category": {"kanji": "体験学習", "hiragana": "たいけんがくしゅう"},
                    "content": {"kanji": "農業・園芸の体験に参加する", "hiragana": "のうぎょう・えんげいの　たいけんに　さんかする"},
                    "daily_action": {"kanji": "近くの農園や園芸教室を調べてみよう 🌱", "hiragana": "ちかくの　のうえん　や　えんげいきょうしつを　しらべてみよう 🌱"},
                },
                {
                    "category": {"kanji": "職場体験", "hiragana": "しょくばたいけん"},
                    "content": {"kanji": "福祉的就労やジョブコーチとの連携を調べる", "hiragana": "ふくしてきしゅうろう　や　ジョブコーチとの　れんけいを　しらべる"},
                    "daily_action": {"kanji": "支援員さんに「職場体験したい」と伝えてみよう 🤝", "hiragana": "しえんいんさんに　「しょくばたいけんしたい」と　つたえてみよう 🤝"},
                },
                {
                    "category": {"kanji": "自己PR", "hiragana": "じこPR"},
                    "content": {"kanji": "自分の強みを短く言えるようにする", "hiragana": "じぶんの　つよみを　みじかく　いえるようにする"},
                    "daily_action": {"kanji": "「私は○○が得意です」と鏡に向かって言ってみよう 💪", "hiragana": "「わたしは　○○が　とくいです」と　かがみに　むかって　いってみよう 💪"},
                },
            ],
            "message": {"kanji": "実際の仕事に近い体験をしてみよう！", "hiragana": "じっさいの　しごとに　ちかい　たいけんを　してみよう！"},
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "manufacturing": {
        1: {
            "tasks": [
                {
                    "category": {"kanji": "生活習慣", "hiragana": "せいかつしゅうかん"},
                    "content": {"kanji": "時刻を守る習慣をつける", "hiragana": "じこくを　まもる　しゅうかんを　つける"},
                    "daily_action": {"kanji": "今日は約束の時間にごはんを食べてみよう ⏰", "hiragana": "きょうは　やくそくの　じかんに　ごはんを　たべてみよう ⏰"},
                },
                {
                    "category": {"kanji": "あいさつ", "hiragana": "あいさつ"},
                    "content": {"kanji": "「おはようございます」「お先に失礼します」を練習", "hiragana": "「おはようございます」「おさきに　しつれいします」を　れんしゅう"},
                    "daily_action": {"kanji": "今日家を出るとき・戻るときあいさつしてみよう 👋", "hiragana": "きょう　いえを　でるとき・もどるとき　あいさつしてみよう 👋"},
                },
                {
                    "category": {"kanji": "集中力", "hiragana": "しゅうちゅうりょく"},
                    "content": {"kanji": "一つのことに集中する時間を伸ばす", "hiragana": "ひとつの　ことに　しゅうちゅうする　じかんを　のばす"},
                    "daily_action": {"kanji": "今日は20分何か一つだけに集中してみよう 🎯", "hiragana": "きょうは　20ぷん　なにか　ひとつだけに　しゅうちゅうしてみよう 🎯"},
                },
                {
                    "category": {"kanji": "基礎スキル", "hiragana": "きそすきる"},
                    "content": {"kanji": "手順を守って作業する練習", "hiragana": "てじゅんを　まもって　さぎょうする　れんしゅう"},
                    "daily_action": {"kanji": "今日の片付けを順番どおりにやってみよう 📋", "hiragana": "きょうの　かたづけを　じゅんばん　どおりに　やってみよう 📋"},
                },
            ],
            "message": {"kanji": "手順を守ることが製造の仕事の基本だよ！", "hiragana": "てじゅんを　まもることが　せいぞうのしごとの　きほんだよ！"},
        },
        2: {
            "tasks": [
                {
                    "category": {"kanji": "作業練習", "hiragana": "さぎょうれんしゅう"},
                    "content": {"kanji": "細かいものを丁寧に扱う練習", "hiragana": "こまかい　ものを　ていねいに　あつかう　れんしゅう"},
                    "daily_action": {"kanji": "細かいパズルやレゴを丁寧に組み立ててみよう 🔧", "hiragana": "こまかい　パズルや　レゴを　ていねいに　くみたててみよう 🔧"},
                },
                {
                    "category": {"kanji": "品質確認", "hiragana": "ひんしつかくにん"},
                    "content": {"kanji": "「できた！」のあともう一度確かめる習慣", "hiragana": "「できた！」のあと　もういちど　たしかめる　しゅうかん"},
                    "daily_action": {"kanji": "今日何かをしたあと「間違いないかな？」と見直してみよう 🔍", "hiragana": "きょう　なにかを　したあと　「まちがいないかな？」と　みなおしてみよう 🔍"},
                },
                {
                    "category": {"kanji": "くりかえし作業", "hiragana": "くりかえし さぎょう"},
                    "content": {"kanji": "同じ手順を何度も練習する", "hiragana": "おなじ　てじゅんを　なんども　れんしゅうする"},
                    "daily_action": {"kanji": "紙を折る・塗り絵を塗るなどくりかえす作業をやってみよう ♻️", "hiragana": "かみを　おる・ぬりえを　ぬるなど　くりかえす　さぎょうを　やってみよう ♻️"},
                },
                {
                    "category": {"kanji": "報告", "hiragana": "ほうこく"},
                    "content": {"kanji": "ミスをしたとき、すぐに伝える練習", "hiragana": "ミスをしたとき　すぐに　つたえる　れんしゅう"},
                    "daily_action": {"kanji": "今日失敗したことを正直に人に伝えてみよう 💬", "hiragana": "きょう　しっぱいしたことを　しょうじきに　ひとに　つたえてみよう 💬"},
                },
            ],
            "message": {"kanji": "丁寧さと確認が製造の仕事の最大の武器！", "hiragana": "ていねいさと　かくにんが　せいぞうのしごとの　さいだいの　ぶき！"},
        },
        3: {
            "tasks": [
                {
                    "category": {"kanji": "体験学習", "hiragana": "たいけんがくしゅう"},
                    "content": {"kanji": "製造系の福祉的就労や工場見学に参加する", "hiragana": "せいぞうけいの　ふくしてきしゅうろう　や　こうじょうけんがくに　さんかする"},
                    "daily_action": {"kanji": "支援センターに「工場見学したい」と相談してみよう 🏭", "hiragana": "しえんセンターに　「こうじょうけんがくしたい」と　そうだんしてみよう 🏭"},
                },
                {
                    "category": {"kanji": "職場体験", "hiragana": "しょくばたいけん"},
                    "content": {"kanji": "ライン作業の体験をする", "hiragana": "ラインさぎょうの　たいけんを　する"},
                    "daily_action": {"kanji": "封筒にチラシを入れるなどくりかえし作業をやってみよう 📦", "hiragana": "ふうとうに　ちらしを　いれる　など　くりかえし作業を　やってみよう 📦"},
                },
                {
                    "category": {"kanji": "自己PR", "hiragana": "じこPR"},
                    "content": {"kanji": "「丁寧にできます」を自信を持って言えるようにする", "hiragana": "「ていねいに　できます」を　じしんを　もって　いえるようにする"},
                    "daily_action": {"kanji": "「私は丁寧に作業します」と鏡に言ってみよう 💪", "hiragana": "「わたしは　ていねいに　さぎょうします」と　かがみに　いってみよう 💪"},
                },
            ],
            "message": {"kanji": "実際の工場に近い体験をしよう！", "hiragana": "じっさいの　こうじょうに　ちかい　たいけんを　しよう！"},
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "cleaning": {
        1: {
            "tasks": [
                {
                    "category": {"kanji": "生活習慣", "hiragana": "せいかつしゅうかん"},
                    "content": {"kanji": "自分の部屋を毎日片付ける", "hiragana": "じぶんの　へやを　まいにち　かたづける"},
                    "daily_action": {"kanji": "今日は自分の部屋を5分片付けてみよう 🧹", "hiragana": "きょうは　じぶんの　へやを　5ふん　かたづけてみよう 🧹"},
                },
                {
                    "category": {"kanji": "あいさつ", "hiragana": "あいさつ"},
                    "content": {"kanji": "すれ違う人に「こんにちは」と言える", "hiragana": "すれちがう　ひとに　「こんにちは」と　いえる"},
                    "daily_action": {"kanji": "今日人に会ったら「こんにちは」と言ってみよう 👋", "hiragana": "きょう　ひとに　あったら　「こんにちは」と　いってみよう 👋"},
                },
                {
                    "category": {"kanji": "体力づくり", "hiragana": "たいりょくづくり"},
                    "content": {"kanji": "体を動かす習慣をつける", "hiragana": "からだを　うごかす　しゅうかんを　つける"},
                    "daily_action": {"kanji": "今日は家の周りを10分歩いてみよう 🚶", "hiragana": "きょうは　いえの　まわりを　10ぷん　あるいてみよう 🚶"},
                },
                {
                    "category": {"kanji": "基礎スキル", "hiragana": "きそすきる"},
                    "content": {"kanji": "掃除道具の使い方を覚える", "hiragana": "そうじどうぐの　つかいかたを　おぼえる"},
                    "daily_action": {"kanji": "ほうき・雑巾の使い方を練習してみよう 🧽", "hiragana": "ほうき・ぞうきんの　つかいかたを　れんしゅうしてみよう 🧽"},
                },
            ],
            "message": {"kanji": "きれいにする仕事の基本は自分の周りをきれいにすること！", "hiragana": "きれいにする　しごとの　きほんは　じぶんの　まわりを　きれいにすること！"},
        },
        2: {
            "tasks": [
                {
                    "category": {"kanji": "作業練習", "hiragana": "さぎょうれんしゅう"},
                    "content": {"kanji": "掃除の手順を覚えてくりかえす", "hiragana": "そうじの　てじゅんを　おぼえて　くりかえす"},
                    "daily_action": {"kanji": "トイレや玄関を順番どおりに掃除してみよう 🚿", "hiragana": "トイレや　げんかんを　じゅんばん　どおりに　そうじしてみよう 🚿"},
                },
                {
                    "category": {"kanji": "確認", "hiragana": "かくにん"},
                    "content": {"kanji": "掃除のあと「見残しがないか」確認する", "hiragana": "そうじのあと　「みのこしがないか」　かくにんする"},
                    "daily_action": {"kanji": "今日の掃除のあと汚れが残っていないか見てみよう 🔍", "hiragana": "きょうの　そうじのあと　よごれが　のこっていないか　みてみよう 🔍"},
                },
                {
                    "category": {"kanji": "くりかえし作業", "hiragana": "くりかえし さぎょう"},
                    "content": {"kanji": "同じ掃除を毎日同じ手順でおこなう", "hiragana": "おなじ　そうじを　まいにち　おなじ　てじゅんで　おこなう"},
                    "daily_action": {"kanji": "今日も昨日と同じ手順で掃除してみよう ♻️", "hiragana": "きょうも　きのうと　おなじ　てじゅんで　そうじしてみよう ♻️"},
                },
                {
                    "category": {"kanji": "報告", "hiragana": "ほうこく"},
                    "content": {"kanji": "掃除が終わったら「できました」と点検する", "hiragana": "そうじが　おわったら　「できました」と　てんけんする"},
                    "daily_action": {"kanji": "掃除が終わったら「終わりました！」と言ってみよう ✅", "hiragana": "そうじが　おわったら　「おわりました！」と　いってみよう ✅"},
                },
            ],
            "message": {"kanji": "毎日同じ手順で掃除すると上手になるよ！", "hiragana": "まいにち　おなじ　てじゅんで　そうじすると　じょうずに　なるよ！"},
        },
        3: {
            "tasks": [
                {
                    "category": {"kanji": "体験学習", "hiragana": "たいけんがくしゅう"},
                    "content": {"kanji": "清掃系福祉的就労の体験", "hiragana": "せいそうけい　ふくしてきしゅうろうの　たいけん"},
                    "daily_action": {"kanji": "支援センターに「清掃作業をやってみたい」と伝えよう 🧹", "hiragana": "しえんセンターに　「せいそうさぎょうを　やってみたい」と　つたえよう 🧹"},
                },
                {
                    "category": {"kanji": "職場体験", "hiragana": "しょくばたいけん"},
                    "content": {"kanji": "施設の掃除を手伝う経験をする", "hiragana": "しせつの　そうじを　てつだう　けいけんをする"},
                    "daily_action": {"kanji": "家でみんなが使う場所を一生懸命掃除してみよう 🏢", "hiragana": "いえで　みんなが　つかう　ばしょを　いっしょうけんめい　そうじしてみよう 🏢"},
                },
                {
                    "category": {"kanji": "自己PR", "hiragana": "じこPR"},
                    "content": {"kanji": "「きれいにする仕事が好きです」と言えるようにする", "hiragana": "「きれいにする　しごとが　すきです」を　いえるようにする"},
                    "daily_action": {"kanji": "「私は掃除が好きです」と人に話してみよう 😊", "hiragana": "「わたしは　そうじが　すきです」と　ひとに　はなしてみよう 😊"},
                },
            ],
            "message": {"kanji": "実際の環境整備の仕事を体験しよう！", "hiragana": "じっさいの　かんきょうせいびの　しごとを　たいけんしよう！"},
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "food_processing": {
        1: {
            "tasks": [
                {
                    "category": {"kanji": "生活習慣", "hiragana": "せいかつしゅうかん"},
                    "content": {"kanji": "毎日決まった時間に食事をとる", "hiragana": "まいにち　きまった　じかんに　しょくじを　とる"},
                    "daily_action": {"kanji": "今日は決まった時間にごはんを食べてみよう 🍚", "hiragana": "きょうは　きまった　じかんに　ごはんを　たべてみよう 🍚"},
                },
                {
                    "category": {"kanji": "衛生習慣", "hiragana": "えいせいしゅうかん"},
                    "content": {"kanji": "手洗いを丁寧におこなう", "hiragana": "てあらいを　ていねいに　おこなう"},
                    "daily_action": {"kanji": "今日は20秒かけて丁寧に手を洗おう 🧼", "hiragana": "きょうは　20びょう　かけて　ていねいに　てを　あらおう 🧼"},
                },
                {
                    "category": {"kanji": "集中力", "hiragana": "しゅうちゅうりょく"},
                    "content": {"kanji": "丁寧にものを扱う習慣をつける", "hiragana": "ていねいに　ものを　あつかう　しゅうかんを　つける"},
                    "daily_action": {"kanji": "今日は食べものを丁寧に扱ってみよう 🍱", "hiragana": "きょうは　たべものを　ていねいに　あつかってみよう 🍱"},
                },
                {
                    "category": {"kanji": "基礎スキル", "hiragana": "きそすきる"},
                    "content": {"kanji": "順番を守って作業する", "hiragana": "じゅんばんを　まもって　さぎょうする"},
                    "daily_action": {"kanji": "料理を手伝うとき決まった手順でやってみよう 👩‍🍳", "hiragana": "りょうりを　てつだうとき　きまった　てじゅんで　やってみよう 👩‍🍳"},
                },
            ],
            "message": {"kanji": "食べものを扱う仕事は清潔さが一番大事！", "hiragana": "たべものを　あつかう　しごとは　せいけつさが　いちばん　だいじ！"},
        },
        2: {
            "tasks": [
                {
                    "category": {"kanji": "作業練習", "hiragana": "さぎょうれんしゅう"},
                    "content": {"kanji": "食べものをきれいに並べる練習", "hiragana": "たべものを　きれいに　ならべる　れんしゅう"},
                    "daily_action": {"kanji": "今日はお菓子や食べものをきれいに並べてみよう 📦", "hiragana": "きょうは　おかしや　たべものを　きれいに　ならべてみよう 📦"},
                },
                {
                    "category": {"kanji": "品質確認", "hiragana": "ひんしつかくにん"},
                    "content": {"kanji": "分量を正しく量る練習", "hiragana": "ぶんりょうを　ただしく　はかる　れんしゅう"},
                    "daily_action": {"kanji": "料理でスプーンを使ってきちんと量ってみよう ⚖️", "hiragana": "りょうりで　さじを　つかって　きちんと　はかってみよう ⚖️"},
                },
                {
                    "category": {"kanji": "くりかえし作業", "hiragana": "くりかえし さぎょう"},
                    "content": {"kanji": "同じ包装・詰める作業をくりかえす", "hiragana": "おなじ　ほうそう・つめる　さぎょうを　くりかえす"},
                    "daily_action": {"kanji": "お菓子を袋に入れる練習をやってみよう 🎁", "hiragana": "おかしを　ふくろに　いれる　れんしゅうを　やってみよう 🎁"},
                },
                {
                    "category": {"kanji": "報告", "hiragana": "ほうこく"},
                    "content": {"kanji": "異常があったとき、すぐ伝える", "hiragana": "いじょうが　あったとき　すぐ　つたえる"},
                    "daily_action": {"kanji": "何か変だと思ったらすぐ人に言う練習をしよう 💬", "hiragana": "なにか　へんだと　おもったら　すぐ　ひとに　いう　れんしゅうを　しよう 💬"},
                },
            ],
            "message": {"kanji": "丁寧さと規制を守ることが食品の仕事の要！", "hiragana": "ていねいさと　きせいを　まもることが　しょくひんのしごとの　かなめ！"},
        },
        3: {
            "tasks": [
                {
                    "category": {"kanji": "体験学習", "hiragana": "たいけんがくしゅう"},
                    "content": {"kanji": "食品加工の福祉的就労を体験する", "hiragana": "しょくひんかこうの　ふくしてきしゅうろうを　たいけんする"},
                    "daily_action": {"kanji": "支援センターに「食品の仕事をやってみたい」と言おう 🍱", "hiragana": "しえんセンターに　「しょくひんのしごとを　やってみたい」と　いおう 🍱"},
                },
                {
                    "category": {"kanji": "職場体験", "hiragana": "しょくばたいけん"},
                    "content": {"kanji": "お弁当や惣菜を作る経験をする", "hiragana": "おべんとうや　そうざいを　つくる　けいけんをする"},
                    "daily_action": {"kanji": "家で簡単なお弁当を自分で作ってみよう 🍙", "hiragana": "いえで　かんたんな　おべんとうを　じぶんで　つくってみよう 🍙"},
                },
                {
                    "category": {"kanji": "自己PR", "hiragana": "じこPR"},
                    "content": {"kanji": "「丁寧できれい好きです」を言えるようにする", "hiragana": "「ていねいで　きれいずきです」を　いえるようにする"},
                    "daily_action": {"kanji": "「私は丁寧に作業できます」と練習しよう 💪", "hiragana": "「わたしは　ていねいに　さぎょうできます」と　れんしゅうしよう 💪"},
                },
            ],
            "message": {"kanji": "食品加工の仕事を体験して向いているか確かめよう！", "hiragana": "しょくひんかこうの　しごとを　たいけんして　むいているか　たしかめよう！"},
        },
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "service": {
        1: {
            "tasks": [
                {
                    "category": {"kanji": "あいさつ", "hiragana": "あいさつ"},
                    "content": {"kanji": "「いらっしゃいませ」「ありがとうございます」を練習", "hiragana": "「いらっしゃいませ」「ありがとうございます」を　れんしゅう"},
                    "daily_action": {"kanji": "今日家で「いらっしゃいませ」と高い声で言ってみよう 😊", "hiragana": "きょう　いえで　「いらっしゃいませ」と　たかい　こえで　いってみよう 😊"},
                },
                {
                    "category": {"kanji": "コミュニケーション", "hiragana": "コミュニケーション"},
                    "content": {"kanji": "人の話を最後まで聞く練習", "hiragana": "ひとの　はなしを　さいごまで　きく　れんしゅう"},
                    "daily_action": {"kanji": "今日誰かが話しているとき最後まで聞いてみよう 👂", "hiragana": "きょう　だれかが　はなしているとき　さいごまで　きいてみよう 👂"},
                },
                {
                    "category": {"kanji": "生活習慣", "hiragana": "せいかつしゅうかん"},
                    "content": {"kanji": "見た目をきちんと整える習慣をつける", "hiragana": "みためを　きちんと　ととのえる　しゅうかんを　つける"},
                    "daily_action": {"kanji": "今日は髪をとかして服をきれいに着てみよう 👔", "hiragana": "きょうは　かみを　とかして　ふくを　きれいに　きてみよう 👔"},
                },
                {
                    "category": {"kanji": "基礎スキル", "hiragana": "きそすきる"},
                    "content": {"kanji": "「すみません」「ありがとう」を自然に言えるようにする", "hiragana": "「すみません」「ありがとう」を　しぜんに　いえるようにする"},
                    "daily_action": {"kanji": "今日は3回「ありがとう」を使ってみよう 🙏", "hiragana": "きょうは　3かい　「ありがとう」を　つかってみよう 🙏"},
                },
            ],
            "message": {"kanji": "笑顔とあいさつが接客の仕事の一番の武器！", "hiragana": "えがおと　あいさつが　せっきゃくのしごとの　いちばんの　ぶき！"},
        },
        2: {
            "tasks": [
                {
                    "category": {"kanji": "接客練習", "hiragana": "せっきゃくれんしゅう"},
                    "content": {"kanji": "丁寧な言葉を使って答える練習", "hiragana": "ていねいな　ことばを　つかって　こたえる　れんしゅう"},
                    "daily_action": {"kanji": "家で「いらっしゃいませ、何かお手伝いしますか？」と練習しよう 🛒", "hiragana": "いえで　「いらっしゃいませ、なにか　おてつだいしますか？」と　れんしゅうしよう 🛒"},
                },
                {
                    "category": {"kanji": "商品陳列", "hiragana": "しょうひんちんれつ"},
                    "content": {"kanji": "ものをきれいに並べる練習", "hiragana": "ものを　きれいに　ならべる　れんしゅう"},
                    "daily_action": {"kanji": "今日は本棚や冷蔵庫をきれいに並べ直してみよう 📦", "hiragana": "きょうは　ほんだなや　れいぞうこを　きれいに　ならべなおしてみよう 📦"},
                },
                {
                    "category": {"kanji": "気づく力", "hiragana": "きづくちから"},
                    "content": {"kanji": "「人に気づいたら声をかける」練習", "hiragana": "「ひとに　きづいたら　こえをかける」れんしゅう"},
                    "daily_action": {"kanji": "困っている人に気づいたら「何かお手伝いしましょうか？」と言ってみよう 💬", "hiragana": "こまっている　ひとに　きづいたら　「なにか　おてつだいしましょうか？」と　いってみよう 💬"},
                },
                {
                    "category": {"kanji": "報告", "hiragana": "ほうこく"},
                    "content": {"kanji": "わからないとき「教えてください」と言えるようにする", "hiragana": "わからないとき　「おしえてください」と　いえるようにする"},
                    "daily_action": {"kanji": "今日わからないことを「教えてください」と言ってみよう 🙋", "hiragana": "きょう　わからないことを　「おしえてください」と　いってみよう 🙋"},
                },
            ],
            "message": {"kanji": "人にやさしく声をかけることが接客の仕事の鍵！", "hiragana": "ひとに　やさしく　こえをかけることが　せっきゃくのしごとの　かぎ！"},
        },
        3: {
            "tasks": [
                {
                    "category": {"kanji": "体験学習", "hiragana": "たいけんがくしゅう"},
                    "content": {"kanji": "接客・販売補助の福祉的就労を体験する", "hiragana": "せっきゃく・はんばいほじょの　ふくしてきしゅうろうを　たいけんする"},
                    "daily_action": {"kanji": "支援センターに「お店の仕事を体験したい」と伝えよう 🛒", "hiragana": "しえんセンターに　「おみせのしごとを　たいけんしたい」と　つたえよう 🛒"},
                },
                {
                    "category": {"kanji": "職場体験", "hiragana": "しょくばたいけん"},
                    "content": {"kanji": "ショッピングモールやスーパーで仕事を見る", "hiragana": "しょっぴんぐモールや　スーパーで　しごとを　みる"},
                    "daily_action": {"kanji": "スーパーで店員さんの仕事をじっくり見てみよう 🏪", "hiragana": "スーパーで　てんいんさんの　しごとを　じっくり　みてみよう 🏪"},
                },
                {
                    "category": {"kanji": "自己PR", "hiragana": "じこPR"},
                    "content": {"kanji": "「笑顔で働けます」を自信を持って言えるようにする", "hiragana": "「えがおで　はたらけます」を　じしんを　もって　いえるようにする"},
                    "daily_action": {"kanji": "鏡に向かって笑顔で「よろしくお願いします！」と言ってみよう 😊", "hiragana": "かがみに　むかって　えがおで　「よろしくおねがいします！」と　いってみよう 😊"},
                },
            ],
            "message": {"kanji": "笑顔で働けるあなたがお店の大切な力になるよ！", "hiragana": "えがおで　はたらける　あなたが　おみせの　たいせつな　ちからに　なるよ！"},
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
            "message": step_data.get("message", {"kanji": "一歩一歩頑張ろう！", "hiragana": "いっぽ　いっぽ　がんばろう！"}),
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

        latest = daily_records[0]
        if latest.emotion_stamp >= 4:
            return "最近きもちが安定しているようです。この調子を応援しつつ、次のステップへの声かけをしてみましょう。"
        elif latest.emotion_stamp <= 2:
            return "最近つらそうな日が続いています。ゆっくり話を聞く時間をとってみましょう。焦らず寄り添うことが大切です。"
        else:
            return "記録が続いています！毎日記録できていることを褒めてあげましょう。小さな成功体験が積み重なります。"
