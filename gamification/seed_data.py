"""週間チャレンジ・クイズの初期データを投入するスクリプト"""
from gamification.models import WeeklyChallenge
from learning.models import MannerQuiz, QuizChoice

CHALLENGES = [
    (1, '🔥 3日間ログインしよう', '3日続けてアプリを開こう！', 'login', 3, 50),
    (2, '📒 記録を3回つけよう', '今週3回、今日の記録をつけよう！', 'record', 3, 60),
    (3, '🎓 クイズを5問解こう', '就労マナークイズに挑戦しよう！', 'quiz', 5, 70),
    (4, '🔄 診断を受けよう', '今週1回、診断にチャレンジ！', 'diagnosis', 1, 80),
    (5, '💬 AIに相談しよう', 'AIアバターと1回話してみよう', 'chat', 1, 60),
]

QUIZZES = [
    # 挨拶・言葉遣い
    {
        'category': 'greeting', 'emoji': '👋', 'order': 1,
        'question': '朝、職場に着いたら何と言いますか？',
        'explanation': '「おはようございます」は社会人の基本の挨拶です。',
        'choices': [
            ('おはようございます', True),
            ('こんにちは', False),
            ('よろしくおねがいします', False),
            ('何も言わない', False),
        ]
    },
    {
        'category': 'greeting', 'emoji': '🙏', 'order': 2,
        'question': '仕事でミスをしてしまった。まず何をする？',
        'explanation': 'ミスをしたらすぐに「申し訳ありません」と謝り、上司に報告しましょう。',
        'choices': [
            ('上司に報告して謝る', True),
            ('黙って直す', False),
            ('その場を離れる', False),
            ('誰かのせいにする', False),
        ]
    },
    # 報連相
    {
        'category': 'report', 'emoji': '📢', 'order': 1,
        'question': '作業が終わったとき、何と言いますか？',
        'explanation': '「報告」は仕事の基本。「○○が終わりました」と上司に伝えましょう。',
        'choices': [
            ('「終わりました。次は何をしますか？」と聞く', True),
            ('黙って次の仕事を探す', False),
            ('休憩する', False),
            ('帰る', False),
        ]
    },
    {
        'category': 'report', 'emoji': '🆘', 'order': 2,
        'question': 'わからないことがあったとき、どうしますか？',
        'explanation': '「わかりません」「教えてください」と言うのはとても大事なことです。',
        'choices': [
            ('上司や先輩に「教えてください」と聞く', True),
            ('わかったふりをして進める', False),
            ('何もしないで待つ', False),
            ('その仕事をやめる', False),
        ]
    },
    # ビジネスマナー
    {
        'category': 'manner', 'emoji': '⏰', 'order': 1,
        'question': '仕事の開始時間が9時の場合、何時までに着けばよいですか？',
        'explanation': '開始時間の5〜10分前には到着して、準備をしましょう。',
        'choices': [
            ('8時50分〜55分頃', True),
            ('9時ちょうど', False),
            ('9時5分', False),
            ('8時30分（早すぎる場合もある）', False),
        ]
    },
    {
        'category': 'manner', 'emoji': '📱', 'order': 2,
        'question': '仕事中にスマートフォンを使ってよい場面はどれ？',
        'explanation': '仕事中の私用スマホは原則禁止。休憩時間のみ使用しましょう。',
        'choices': [
            ('休憩時間に使う', True),
            ('仕事中に少しだけ', False),
            ('トイレに行ったとき', False),
            ('上司が見ていないとき', False),
        ]
    },
    # 安全・衛生
    {
        'category': 'safety', 'emoji': '🧼', 'order': 1,
        'question': '食品を扱う仕事で、作業前に必ずすることは？',
        'explanation': '食品を扱う前は必ず手を洗い、衛生管理を徹底しましょう。',
        'choices': [
            ('手洗い・消毒をする', True),
            ('すぐに作業を始める', False),
            ('手袋だけつける', False),
            ('特に何もしない', False),
        ]
    },
    # チームワーク
    {
        'category': 'team', 'emoji': '🤝', 'order': 1,
        'question': '同僚が困っているとき、どうする？',
        'explanation': 'チームで助け合うことが大切。声をかけてみましょう。',
        'choices': [
            ('「何か手伝えますか？」と声をかける', True),
            ('関係ないので無視する', False),
            ('上司だけに任せる', False),
            ('後で聞く', False),
        ]
    },
]


def run():
    # 週間チャレンジ
    for week, title, desc, ttype, count, points in CHALLENGES:
        WeeklyChallenge.objects.get_or_create(
            week_number=week,
            defaults=dict(title=title, description=desc, target_type=ttype,
                         target_count=count, reward_points=points)
        )

    # クイズ
    for q_data in QUIZZES:
        quiz, created = MannerQuiz.objects.get_or_create(
            category=q_data['category'],
            question=q_data['question'],
            defaults=dict(
                emoji=q_data['emoji'],
                explanation=q_data['explanation'],
                order=q_data['order']
            )
        )
        if created:
            for i, (text, correct) in enumerate(q_data['choices']):
                QuizChoice.objects.create(quiz=quiz, text=text, is_correct=correct, order=i)

    print(f"Challenges: {WeeklyChallenge.objects.count()}")
    print(f"Quizzes: {MannerQuiz.objects.count()}")
