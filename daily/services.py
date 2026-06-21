import random
from django.conf import settings
from roadmap.services import resolve_data


JOB_TYPE_LABELS = {
    'agriculture': '農業・園芸系',
    'manufacturing': '製造・組み立て系',
    'cleaning': '清掃・環境整備系',
    'food_processing': '食品加工系',
    'service': '接客・販売補助系',
}


def get_avatar_system_prompt(profile, text_mode: str = 'hiragana') -> str:
    """ユーザーのプロフィール・診断結果からアバターのシステムプロンプトを生成"""
    from diagnosis.models import DiagnosisSession

    nickname = profile.nickname
    job_type = '仕事'
    strengths = '一生懸命なこと'
    challenges = 'むずかしいことがあること'

    try:
        session = DiagnosisSession.objects.filter(
            session_key__startswith='user_'
        ).order_by('-created_at').first()
        if session and session.job_type:
            job_type = JOB_TYPE_LABELS.get(session.job_type, session.job_type)
            strengths_list = session.get_strengths()
            challenges_list = session.get_challenges()
            if strengths_list:
                strengths = '、'.join(strengths_list[:3])
            if challenges_list:
                challenges = '、'.join(challenges_list[:2])
    except Exception:
        pass

    if text_mode == 'kanji':
        text_mode_instruction = '漢字を使った読みやすい文章で話してください。'
    else:
        text_mode_instruction = 'できるだけひらがなを使って、やさしい言葉で話してください。'

    return f"""あなたは{nickname}さん自身の分身のアバターです。
{nickname}さんは{job_type}の仕事を目指しており、
強みは「{strengths}」、課題は「{challenges}」です。

あなたの役割：
- {nickname}さんの気持ちに共感する
- 就労に向けた小さな一歩を一緒に考える
- 否定せず、できることに注目する
- やさしく、短い文章で話す（2〜3文以内）
- {text_mode_instruction}

話し方：「だよ」「だね」「いっしょにかんがえよう」など親しみやすく。
相手を励ますとき、無理にポジティブにしすぎず、気持ちに寄り添うこと。"""


def chat_with_avatar(profile, user_message: str, text_mode: str = 'hiragana') -> str:
    """OpenAI API を使ってアバターと会話する。失敗時はフォールバック"""
    from .models import AvatarChatMessage

    if not settings.OPENAI_API_KEY:
        return _fallback_avatar_response(user_message, profile, text_mode)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = get_avatar_system_prompt(profile, text_mode)

        recent_messages = AvatarChatMessage.objects.filter(
            profile=profile
        ).order_by('-created_at')[:10]
        history = list(reversed(recent_messages))

        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            role = "user" if msg.role == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except Exception:
        return _fallback_avatar_response(user_message, profile, text_mode)


def _fallback_avatar_response(user_message: str, profile, text_mode: str = 'hiragana') -> str:
    """APIなしの場合のルールベース返答"""
    msg_lower = user_message.lower()

    patterns = [
        (
            ['つかれた', '疲れた', 'しんどい', 'つらい', '辛い', 'きつい'],
            {
                'hiragana': [
                    'むりしなくていいよ。きょうはゆっくりやすもう🌿',
                    'つかれたんだね。よくがんばったよ。すこしやすんで🍵',
                ],
                'kanji': [
                    '無理しなくていいよ。今日はゆっくり休もう🌿',
                    '疲れたんだね。よく頑張ったよ。少し休んで🍵',
                ],
            },
        ),
        (
            ['できた', '出来た', 'うまくいった', 'よかった', '成功', 'せいこう'],
            {
                'hiragana': [
                    'すごい！よくがんばったね！✨',
                    'やったね！それはうれしいね😊',
                ],
                'kanji': [
                    'すごい！よく頑張ったね！✨',
                    'やったね！それは嬉しいね😊',
                ],
            },
        ),
        (
            ['むずかしい', '難しい', 'わからない', 'わかんない', 'できない'],
            {
                'hiragana': [
                    'いっしょにかんがえよう。なにがむずかしかった？🤔',
                    'むずかしいよね。ひとつずつやってみよう💪',
                ],
                'kanji': [
                    '一緒に考えよう。何が難しかった？🤔',
                    '難しいよね。一つずつやってみよう💪',
                ],
            },
        ),
        (
            ['ふあん', '不安', 'こわい', '怖い', 'しんぱい', '心配'],
            {
                'hiragana': [
                    'ふあんなきもち、はなしてくれてありがとう🌸',
                    'そのきもち、わかるよ。いっしょにいるよ🤝',
                ],
                'kanji': [
                    '不安な気持ち、話してくれてありがとう🌸',
                    'その気持ち、わかるよ。一緒にいるよ🤝',
                ],
            },
        ),
        (
            ['たのしい', '楽しい', 'うれしい', '嬉しい', 'よかった'],
            {
                'hiragana': [
                    'それはよかった！きいてうれしいよ😄',
                    'たのしかったんだね！もっとおしえて✨',
                ],
                'kanji': [
                    'それは良かった！聞いて嬉しいよ😄',
                    '楽しかったんだね！もっと教えて✨',
                ],
            },
        ),
    ]

    for keywords, responses in patterns:
        if any(kw in msg_lower for kw in keywords):
            options = responses.get(text_mode, responses['hiragana'])
            return random.choice(options)

    defaults = {
        'hiragana': [
            'そうなんだね。もうすこしおしえて？🌱',
            'うん、きいてるよ。どんなことがあったの？',
        ],
        'kanji': [
            'そうなんだね。もう少し教えて？🌱',
            'うん、聞いてるよ。どんなことがあったの？',
        ],
    }
    options = defaults.get(text_mode, defaults['hiragana'])
    return random.choice(options)


def get_supporter_advice(user_profile, daily_records, text_mode: str = 'hiragana') -> str:
    """支援者向けAIアドバイスを生成（フォールバックあり）"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        records_text = ""
        for r in daily_records[:7]:
            records_text += (
                f"- {r.date}: きもち「{r.get_emotion_label()}」, "
                f"からだ「{r.get_health_label()}」\n"
                f"  できたこと：{r.did_well[:30] if r.did_well else '（記録なし）'}\n"
            )

        prompt = f"""就労支援の支援者として、以下の利用者の1週間の記録を見てアドバイスをください。
やさしい言葉で、支援者に向けた具体的なアドバイスを2〜3文で。

利用者ニックネーム: {user_profile.nickname}
記録:
{records_text if records_text else '（記録なし）'}

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
            return resolve_data(
                {
                    "kanji": "まだ記録がありません。利用者に日々の記録をつけるよう声かけしてみましょう。",
                    "hiragana": "まだ きろくが ありません。りようしゃに ひびの きろくを つけるよう こえかけして みましょう。",
                },
                text_mode,
            )

        latest = daily_records[-1]
        if latest.emotion_stamp >= 4:
            return resolve_data(
                {
                    "kanji": "最近きもちが安定しているようです！この調子を応援しながら、次のステップへの声かけをしてみましょう。",
                    "hiragana": "さいきん きもちが あんていして いるようです！この ちょうしを おうえんしながら、つぎの ステップへの こえかけを してみましょう。",
                },
                text_mode,
            )
        elif latest.emotion_stamp <= 2:
            return resolve_data(
                {
                    "kanji": "最近つらそうな日が続いています。ゆっくり話を聞く時間をとりましょう。焦らず寄り添うことが大切です。",
                    "hiragana": "さいきん つらそうな ひが つづいています。ゆっくり はなしを きく じかんを とりましょう。あせらず よりそうことが たいせつです。",
                },
                text_mode,
            )
        else:
            return resolve_data(
                {
                    "kanji": "記録が続いています！毎日記録できていることを褒めてあげましょう。小さな成功体験の積み重ねが大切です。",
                    "hiragana": "きろくが つづいています！まいにち きろくできていることを ほめてあげましょう。ちいさな せいこうたいけんの つみかさねが たいせつです。",
                },
                text_mode,
            )
