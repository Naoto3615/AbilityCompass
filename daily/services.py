import json
from django.conf import settings
from django.utils import timezone
from .models import DailyTask, TASK_CATEGORIES, TASK_CATEGORY_EMOJIS


def generate_daily_tasks(profile) -> list:
    """今日のタスクをAIで生成（またはフォールバック）"""
    today = timezone.localdate()

    existing = DailyTask.objects.filter(profile=profile, date=today)
    if existing.exists():
        return list(existing)

    career_name = profile.career_goal_name or 'まだ決まっていない'
    age_label = profile.get_age_group_label()

    tasks_data = _generate_with_ai(career_name, age_label, profile.age_group, profile.career_goal)

    tasks = []
    for item in tasks_data[:5]:
        task = DailyTask.objects.create(
            profile=profile,
            date=today,
            category=item['category'],
            content=item['content'],
            points=item.get('points', 10),
        )
        tasks.append(task)

    return tasks


def _generate_with_ai(career_name: str, age_label: str, age_group_key: str, career_key: str = '') -> list:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = f"""発達障害を持つ子供向けの、今日1日でできる小さなタスクを5つ提案してください。

目標職業：{career_name}
年齢フェーズ：{age_label}

以下のカテゴリから1つずつ選んでください：
- learning（学習・スキル）
- character（人間性・心の成長）
- habit（日々の習慣）
- social（コミュニケーション）
- strength（強みを活かす活動）

JSON形式で返してください：
{{
  "tasks": [
    {{"category": "learning", "content": "タスク内容（30文字以内、具体的で今日できる小さなこと）", "points": 10}},
    {{"category": "character", "content": "...", "points": 10}},
    {{"category": "habit", "content": "...", "points": 10}},
    {{"category": "social", "content": "...", "points": 10}},
    {{"category": "strength", "content": "...", "points": 15}}
  ]
}}

注意：
- 発達障害の特性を考慮した現実的で達成しやすい内容にする
- ポジティブな表現で書く
- 子供が1日でできる小さなステップにする"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return data.get('tasks', [])

    except Exception:
        return _fallback_tasks(age_group_key, career_key)


_CAREER_TASKS = {
    'programmer': {
        'early_childhood': [
            {'category': 'learning',  'content': 'パズルや積み木で「順番どおり」に並べる遊びをする', 'points': 10},
            {'category': 'character', 'content': 'うまくいかなくても「もう1回！」と言う練習', 'points': 10},
            {'category': 'habit',     'content': '決まった時間にやることを自分でやってみる', 'points': 10},
            {'category': 'social',    'content': '作ったものを家族に見せて説明する', 'points': 10},
            {'category': 'strength',  'content': 'Scratch Jr で好きなキャラクターを動かしてみる', 'points': 15},
        ],
        'lower_elementary': [
            {'category': 'learning',  'content': 'Scratch で「動くキャラクター」を1つ作る', 'points': 10},
            {'category': 'character', 'content': 'バグを見つけたら「なぜ？」と考えてみる', 'points': 10},
            {'category': 'habit',     'content': '今日やることをリストにして 1 つずつ消す', 'points': 10},
            {'category': 'social',    'content': '作った作品を友達か家族に遊んでもらう', 'points': 10},
            {'category': 'strength',  'content': '身の回りの機械の「仕組み」を 1 つ調べる', 'points': 15},
        ],
        'upper_elementary': [
            {'category': 'learning',  'content': 'Python でプログラムを 10 行書いて動かす', 'points': 10},
            {'category': 'character', 'content': 'エラーを読んで自力で直す練習をする', 'points': 10},
            {'category': 'habit',     'content': '30 分コーディングに集中する（スマホはしまう）', 'points': 10},
            {'category': 'social',    'content': 'Stack Overflow か教科書で疑問を自分で調べる', 'points': 10},
            {'category': 'strength',  'content': '解決したい「問題」を 1 つ決めてアイデアをメモする', 'points': 15},
        ],
        'middle_school': [
            {'category': 'learning',  'content': 'Python か JavaScript で関数を 1 つ実装する', 'points': 10},
            {'category': 'character', 'content': '昨日書いたコードを読み直して改善点を 1 つ見つける', 'points': 10},
            {'category': 'habit',     'content': 'GitHub に今日のコードを 1 コミット push する', 'points': 10},
            {'category': 'social',    'content': 'Qiita か技術ブログの記事を 1 本読んでコメントする', 'points': 10},
            {'category': 'strength',  'content': 'ポートフォリオ用の作品に今日 1 機能追加する', 'points': 15},
        ],
        'high_school': [
            {'category': 'learning',  'content': '技術書や公式ドキュメントを 20 分読む', 'points': 10},
            {'category': 'character', 'content': '「なぜこの設計にしたか」を言葉で書いてみる', 'points': 10},
            {'category': 'habit',     'content': '毎日 1 commit の習慣を守る', 'points': 10},
            {'category': 'social',    'content': 'OSS の issue を 1 つ読んで理解する', 'points': 10},
            {'category': 'strength',  'content': 'ポートフォリオに今日の成果物を追加・更新する', 'points': 15},
        ],
        'adult': [
            {'category': 'learning',  'content': '専門技術の最新記事や論文を 1 本読む', 'points': 10},
            {'category': 'character', 'content': 'レビューをもらったコードを謙虚に見直す', 'points': 10},
            {'category': 'habit',     'content': '今日の開発時間と進捗をログに残す', 'points': 10},
            {'category': 'social',    'content': 'チームメンバーの質問に 1 回丁寧に答える', 'points': 10},
            {'category': 'strength',  'content': '自分の専門領域で後輩に 1 つ教える', 'points': 15},
        ],
    },
    'designer': {
        'early_childhood': [
            {'category': 'learning',  'content': '好きな色を 3 色選んで絵を描く', 'points': 10},
            {'category': 'character', 'content': '「きれいだな」と思ったものを家族に伝える', 'points': 10},
            {'category': 'habit',     'content': 'スケッチブックに今日 1 ページ描く', 'points': 10},
            {'category': 'social',    'content': '作った絵を家族に見せて感想を聞く', 'points': 10},
            {'category': 'strength',  'content': '外で「かっこいい形」を 1 つ見つけてスケッチする', 'points': 15},
        ],
        'lower_elementary': [
            {'category': 'learning',  'content': 'Canva で簡単なカードを 1 枚デザインする', 'points': 10},
            {'category': 'character', 'content': '「なぜこのデザインが好きか」を言葉にする', 'points': 10},
            {'category': 'habit',     'content': '今日見たデザイン（ポスター・パッケージ）を 1 つ記録する', 'points': 10},
            {'category': 'social',    'content': '作ったデザインを友達か家族に見てもらい感想を聞く', 'points': 10},
            {'category': 'strength',  'content': 'お気に入りのデザインを模写してみる', 'points': 15},
        ],
        'upper_elementary': [
            {'category': 'learning',  'content': 'Canva か Figma でレイアウトを 1 つ作る', 'points': 10},
            {'category': 'character', 'content': '作品の「改善できる点」を 1 つ自分で見つける', 'points': 10},
            {'category': 'habit',     'content': 'Pinterest で今日のインスピレーション画像を 5 枚集める', 'points': 10},
            {'category': 'social',    'content': 'デザインを誰かに見せて「わかりやすいか」を確認する', 'points': 10},
            {'category': 'strength',  'content': 'ポートフォリオ用の作品を 1 点追加する', 'points': 15},
        ],
        'middle_school': [
            {'category': 'learning',  'content': 'Figma でコンポーネントを 1 つ作る', 'points': 10},
            {'category': 'character', 'content': '「使う人の目線」でデザインを 1 点見直す', 'points': 10},
            {'category': 'habit',     'content': '毎日 1 点のデザイン作業を続ける', 'points': 10},
            {'category': 'social',    'content': 'Behance か Instagram にデザインを 1 点投稿する', 'points': 10},
            {'category': 'strength',  'content': 'コンペ・コンテストの情報を調べて応募候補を 1 つ選ぶ', 'points': 15},
        ],
        'high_school': [
            {'category': 'learning',  'content': 'HTML/CSS でデザインを実装する練習を 20 分する', 'points': 10},
            {'category': 'character', 'content': '「なぜこのデザインにしたか」を文章で説明する', 'points': 10},
            {'category': 'habit',     'content': 'ポートフォリオサイトを今日 1 点更新する', 'points': 10},
            {'category': 'social',    'content': 'SNS でデザイン作品を公開してフィードバックをもらう', 'points': 10},
            {'category': 'strength',  'content': 'デザインアワードに応募する作品を 1 点制作する', 'points': 15},
        ],
        'adult': [
            {'category': 'learning',  'content': 'UI/UX の最新トレンドを 1 記事読む', 'points': 10},
            {'category': 'character', 'content': 'クライアントの意図を正確に読み取る練習をする', 'points': 10},
            {'category': 'habit',     'content': '今日のデザイン作業と気づきをログに残す', 'points': 10},
            {'category': 'social',    'content': 'デザインコミュニティで他者の作品にコメントする', 'points': 10},
            {'category': 'strength',  'content': '自分のデザインスタイルを 1 文で言語化してみる', 'points': 15},
        ],
    },
    'musician': {
        'early_childhood': [
            {'category': 'learning',  'content': '好きな曲を最後まで聴いてリズムを手拍子する', 'points': 10},
            {'category': 'character', 'content': '音楽を聴いて感じた気持ちを言葉にする', 'points': 10},
            {'category': 'habit',     'content': '今日 10 分、楽器か歌の練習をする', 'points': 10},
            {'category': 'social',    'content': '好きな曲を家族に聴かせる', 'points': 10},
            {'category': 'strength',  'content': '好きなメロディーを口ずさんでみる', 'points': 15},
        ],
        'lower_elementary': [
            {'category': 'learning',  'content': '楽器の練習を 20 分続ける', 'points': 10},
            {'category': 'character', 'content': '間違えても止まらず最後まで弾く練習をする', 'points': 10},
            {'category': 'habit',     'content': '練習した日をカレンダーにシールで記録する', 'points': 10},
            {'category': 'social',    'content': '練習した曲を家族に聴いてもらう', 'points': 10},
            {'category': 'strength',  'content': '好きな曲の「好きな部分」を繰り返し練習する', 'points': 15},
        ],
        'upper_elementary': [
            {'category': 'learning',  'content': '練習曲を録音して聴き直し、1 つ改善点を見つける', 'points': 10},
            {'category': 'character', 'content': 'うまくいかない部分を「面白い課題」として練習する', 'points': 10},
            {'category': 'habit',     'content': '今日 30 分の練習を集中してやり切る', 'points': 10},
            {'category': 'social',    'content': '音楽仲間か先生に演奏を聴いてもらい感想をもらう', 'points': 10},
            {'category': 'strength',  'content': 'GarageBand で短いメロディーを作ってみる', 'points': 15},
        ],
        'middle_school': [
            {'category': 'learning',  'content': '音楽理論（スケール・コード）を 1 つ覚える', 'points': 10},
            {'category': 'character', 'content': '今日の練習で「昨日より良くなった点」を 1 つ書く', 'points': 10},
            {'category': 'habit',     'content': '毎日 1 時間の練習を必ずやる', 'points': 10},
            {'category': 'social',    'content': 'バンド or 合奏の練習でメンバーに合わせる練習をする', 'points': 10},
            {'category': 'strength',  'content': 'オリジナルフレーズを 1 つ作って録音する', 'points': 15},
        ],
        'high_school': [
            {'category': 'learning',  'content': '専門的な楽曲を 1 曲分析してノートにまとめる', 'points': 10},
            {'category': 'character', 'content': 'ステージ本番をイメージして通し練習をする', 'points': 10},
            {'category': 'habit',     'content': '毎日 2 時間の練習コンディションを維持する', 'points': 10},
            {'category': 'social',    'content': 'SNS か SoundCloud に演奏を 1 本アップする', 'points': 10},
            {'category': 'strength',  'content': 'オリジナル曲の制作を今日 1 パート進める', 'points': 15},
        ],
        'adult': [
            {'category': 'learning',  'content': '音楽ビジネス・著作権について 1 記事読む', 'points': 10},
            {'category': 'character', 'content': '今日の演奏・制作を客観的に振り返る', 'points': 10},
            {'category': 'habit',     'content': '毎日の演奏・制作時間を最優先で確保する', 'points': 10},
            {'category': 'social',    'content': 'リスナーやファンのコメントに 1 件返信する', 'points': 10},
            {'category': 'strength',  'content': '自分の音楽的アイデンティティを 1 文で表現してみる', 'points': 15},
        ],
    },
    'doctor': {
        'early_childhood': [
            {'category': 'learning',  'content': '体の部位（手・足・心臓など）を絵本で調べる', 'points': 10},
            {'category': 'character', 'content': '困っているお友達に「大丈夫？」と声をかける', 'points': 10},
            {'category': 'habit',     'content': '手洗い・うがいを丁寧に 3 回やる', 'points': 10},
            {'category': 'social',    'content': '家族の体調を気にかけて声をかける', 'points': 10},
            {'category': 'strength',  'content': '生き物（植物・虫）の様子を観察してノートに書く', 'points': 15},
        ],
        'lower_elementary': [
            {'category': 'learning',  'content': '人体図鑑を 1 ページ読んで面白いことを 1 つメモする', 'points': 10},
            {'category': 'character', 'content': '友達が悲しそうなとき「一緒にいるよ」と伝える', 'points': 10},
            {'category': 'habit',     'content': '今日の睡眠・食事をきちんと整える', 'points': 10},
            {'category': 'social',    'content': '先生か大人に「なぜ？」の質問を 1 つする', 'points': 10},
            {'category': 'strength',  'content': '理科の実験を楽しんで「なぜそうなるか」を考える', 'points': 15},
        ],
        'upper_elementary': [
            {'category': 'learning',  'content': '理科・算数を 30 分集中して予習する', 'points': 10},
            {'category': 'character', 'content': '「相手の立場」で物事を考える場面を 1 つ実践する', 'points': 10},
            {'category': 'habit',     'content': '毎日 1 時間の学習タイムを守る', 'points': 10},
            {'category': 'social',    'content': 'ボランティアの情報を 1 つ調べて親に相談する', 'points': 10},
            {'category': 'strength',  'content': '医療・健康に関する本やニュースを 1 つ読む', 'points': 15},
        ],
        'middle_school': [
            {'category': 'learning',  'content': '生物・化学の重要単元を 1 つ復習する', 'points': 10},
            {'category': 'character', 'content': 'ストレスを感じたら深呼吸して気持ちを整える', 'points': 10},
            {'category': 'habit',     'content': '毎日 2 時間の学習習慣を今日も守る', 'points': 10},
            {'category': 'social',    'content': '病院・医療関係のボランティアを 1 件調べる', 'points': 10},
            {'category': 'strength',  'content': '医学部受験の情報を 10 分リサーチする', 'points': 15},
        ],
        'high_school': [
            {'category': 'learning',  'content': '生物・化学の模試問題を 1 年分のページ進める', 'points': 10},
            {'category': 'character', 'content': '「なぜ医師になりたいか」を今日 1 文書いてみる', 'points': 10},
            {'category': 'habit',     'content': '今日の学習 3 時間を達成する', 'points': 10},
            {'category': 'social',    'content': '医師・医学生の話を聞ける機会を 1 つ探す', 'points': 10},
            {'category': 'strength',  'content': '小論文のテーマを 1 つ選んで 200 字書いてみる', 'points': 15},
        ],
        'adult': [
            {'category': 'learning',  'content': '医学の最新論文・ガイドラインを 1 つ読む', 'points': 10},
            {'category': 'character', 'content': '患者・スタッフへの対応を今日 1 つ振り返る', 'points': 10},
            {'category': 'habit',     'content': '今日の仕事後に 30 分の自己学習時間を確保する', 'points': 10},
            {'category': 'social',    'content': 'チームメンバーに感謝の言葉を伝える', 'points': 10},
            {'category': 'strength',  'content': '自分の専門性を活かして後輩・患者に 1 つ教える', 'points': 15},
        ],
    },
}

def _fallback_tasks(age_group_key: str, career_key: str = '') -> list:
    if career_key and career_key in _CAREER_TASKS:
        career_age_tasks = _CAREER_TASKS[career_key]
        if age_group_key in career_age_tasks:
            return career_age_tasks[age_group_key]
        return career_age_tasks.get('adult', [])

    generic = {
        'early_childhood': [
            {'category': 'learning',   'content': '好きな絵本を1冊最後まで読む', 'points': 10},
            {'category': 'character',  'content': '「ありがとう」を3回言う', 'points': 10},
            {'category': 'habit',      'content': '朝ごはんを自分で食べる', 'points': 10},
            {'category': 'social',     'content': 'お友達に「おはよう」と言う', 'points': 10},
            {'category': 'strength',   'content': '好きなことを15分とことんやってみる', 'points': 15},
        ],
        'lower_elementary': [
            {'category': 'learning',   'content': '好きな分野の本を15分読む', 'points': 10},
            {'category': 'character',  'content': '失敗しても「次がんばろう」と言う', 'points': 10},
            {'category': 'habit',      'content': '明日の準備を自分でする', 'points': 10},
            {'category': 'social',     'content': '家族に今日あったことを話す', 'points': 10},
            {'category': 'strength',   'content': '好きなことについて20分調べる', 'points': 15},
        ],
        'upper_elementary': [
            {'category': 'learning',   'content': '興味ある本を20分読む', 'points': 10},
            {'category': 'character',  'content': '今日の良かったことを1つ書き出す', 'points': 10},
            {'category': 'habit',      'content': '今日のスケジュールを自分で確認する', 'points': 10},
            {'category': 'social',     'content': '友達や家族に自分の考えを1つ伝える', 'points': 10},
            {'category': 'strength',   'content': '目標の職業に関係することを30分やる', 'points': 15},
        ],
        'middle_school': [
            {'category': 'learning',   'content': '苦手科目を20分集中して勉強する', 'points': 10},
            {'category': 'character',  'content': '感情日記に今日の気持ちを書く', 'points': 10},
            {'category': 'habit',      'content': '22時までに就寝準備を完了する', 'points': 10},
            {'category': 'social',     'content': '誰かに質問・相談を1回してみる', 'points': 10},
            {'category': 'strength',   'content': '目標に関連する動画や記事を1本見る', 'points': 15},
        ],
        'high_school': [
            {'category': 'learning',   'content': '志望校・職業の情報を10分調べる', 'points': 10},
            {'category': 'character',  'content': '今週の振り返りを3行書く', 'points': 10},
            {'category': 'habit',      'content': '今日のタスクリストを朝に作る', 'points': 10},
            {'category': 'social',     'content': '先生や友人に話しかけてみる', 'points': 10},
            {'category': 'strength',   'content': '将来に向けてスキル練習を30分する', 'points': 15},
        ],
        'adult': [
            {'category': 'learning',   'content': '専門スキルを30分学習する', 'points': 10},
            {'category': 'character',  'content': '今日の成長を1つ言葉にする', 'points': 10},
            {'category': 'habit',      'content': '健康的な食事・運動を意識する', 'points': 10},
            {'category': 'social',     'content': '同僚・仲間と1回コミュニケーションをとる', 'points': 10},
            {'category': 'strength',   'content': '自分の強みを活かせる活動を20分する', 'points': 15},
        ],
    }
    return generic.get(age_group_key, generic['lower_elementary'])


def check_and_award_badges(profile):
    """タスク完了後にバッジ付与チェック"""
    from .models import DailyTask, EmotionLog
    from accounts.models import BADGE_DEFINITIONS

    awarded = []

    total_completed = DailyTask.objects.filter(profile=profile, is_completed=True).count()

    if total_completed >= 1:
        if profile.add_badge('first_task'):
            awarded.append(BADGE_DEFINITIONS['first_task'])

    if profile.total_points >= 100:
        if profile.add_badge('points_100'):
            awarded.append(BADGE_DEFINITIONS['points_100'])

    if profile.total_points >= 500:
        if profile.add_badge('points_500'):
            awarded.append(BADGE_DEFINITIONS['points_500'])

    emotion_count = EmotionLog.objects.filter(profile=profile).count()
    if emotion_count >= 5:
        if profile.add_badge('emotion_log_5'):
            awarded.append(BADGE_DEFINITIONS['emotion_log_5'])

    completed_categories = set(
        DailyTask.objects.filter(profile=profile, is_completed=True).values_list('category', flat=True)
    )
    if len(completed_categories) >= 5:
        if profile.add_badge('all_categories'):
            awarded.append(BADGE_DEFINITIONS['all_categories'])

    return awarded


def get_guardian_ai_advice(profile, recent_tasks, recent_emotions) -> str:
    """保護者向けAIアドバイスを生成"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        completed = sum(1 for t in recent_tasks if t.is_completed)
        total = len(recent_tasks)
        avg_emotion = sum(e.score for e in recent_emotions) / len(recent_emotions) if recent_emotions else 3

        prompt = f"""発達障害を持つ子供の保護者へのサポートアドバイスを作成してください。

子供の情報：
- ニックネーム：{profile.nickname}
- 年齢フェーズ：{profile.get_age_group_label()}
- 目標職業：{profile.career_goal_name or '未設定'}
- 直近7日のタスク完了率：{completed}/{total}
- 直近7日の平均気分スコア：{avg_emotion:.1f}/5

この子供の保護者に向けて、以下の内容を含むアドバイスを200文字以内で書いてください：
- 今週の様子への共感
- 具体的なサポートのヒント1〜2つ
- 励ましのメッセージ

温かく専門的なトーンで。"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception:
        return f"{profile.nickname}さんは毎日少しずつ成長しています。完了できた日はしっかり褒めてあげましょう。できなかった日は責めず、「明日またやってみよう」と声をかけてあげることが大切です。"
