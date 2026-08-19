from django.db import models
from django.contrib.auth.models import User


# ─── 就労マナークイズ ──────────────────────────────────────────────────────────

QUIZ_CATEGORIES = [
    ('greeting', '挨拶・言葉遣い'),
    ('report', '報連相'),
    ('manner', 'ビジネスマナー'),
    ('safety', '安全・衛生'),
    ('team', 'チームワーク'),
]


class MannerQuiz(models.Model):
    """就労マナークイズ問題"""
    category = models.CharField('カテゴリ', max_length=20, choices=QUIZ_CATEGORIES)
    question = models.TextField('問題文')
    emoji = models.CharField('絵文字', max_length=10, default='❓')
    explanation = models.TextField('解説', blank=True)
    order = models.IntegerField('順番', default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f"[{self.category}] {self.question[:40]}"


class QuizChoice(models.Model):
    """クイズの選択肢"""
    quiz = models.ForeignKey(MannerQuiz, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField('選択肢', max_length=200)
    is_correct = models.BooleanField('正解', default=False)
    order = models.IntegerField('順番', default=0)

    class Meta:
        ordering = ['order']


class UserQuizResult(models.Model):
    """ユーザーのクイズ回答記録"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(MannerQuiz, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(QuizChoice, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField('正解', default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-answered_at']


# ─── 見通し機能（子ども向け活動スケジュール） ──────────────────────────────────

class DailyScheduleTemplate(models.Model):
    """デイサービスの活動スケジュールテンプレート"""
    name = models.CharField('テンプレート名', max_length=50)
    day_of_week = models.IntegerField('曜日', choices=[
        (0,'月'), (1,'火'), (2,'水'), (3,'木'), (4,'金'), (5,'土'), (6,'日')
    ], default=0)
    is_active = models.BooleanField('有効', default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ScheduleItem(models.Model):
    """スケジュールの各活動"""
    template = models.ForeignKey(DailyScheduleTemplate, on_delete=models.CASCADE, related_name='items')
    time = models.CharField('時刻', max_length=10)  # "09:00"
    activity = models.CharField('活動名', max_length=100)
    emoji = models.CharField('絵文字', max_length=10, default='📍')
    color = models.CharField('色', max_length=20, default='green')
    order = models.IntegerField('順番', default=0)

    class Meta:
        ordering = ['order']


# ─── 連絡帳機能 ──────────────────────────────────────────────────────────────

class ContactNote(models.Model):
    """連絡帳（支援員→保護者・家族）"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_received')
    target_child = models.ForeignKey(
        'daycare.Child', on_delete=models.CASCADE,
        null=True, blank=True, related_name='contact_notes'
    )
    date = models.DateField('対象日')
    mood = models.IntegerField('今日のようす', choices=[
        (5,'とても良かった'), (4,'良かった'), (3,'普通'), (2,'少し心配'), (1,'心配')
    ], default=3)
    content = models.TextField('連絡内容')
    homework = models.TextField('おうちでやってほしいこと', blank=True)
    is_read = models.BooleanField('既読', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date}: {self.from_user.username}→{self.to_user.username}"

    def get_mood_emoji(self):
        return {5:'😄', 4:'😊', 3:'😐', 2:'😟', 1:'😢'}.get(self.mood, '😐')


# ─── 読書記録（子ども向け） ────────────────────────────────────────────────────

class BookRecord(models.Model):
    """読書記録"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_records')
    title = models.CharField('本のタイトル', max_length=200)
    comment = models.TextField('ひとこと感想', blank=True)
    rating = models.IntegerField('評価', choices=[(1,'⭐'),(2,'⭐⭐'),(3,'⭐⭐⭐')], default=3)
    read_at = models.DateField('読んだ日', auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-read_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


# ─── スタンプラリー（子ども向け） ──────────────────────────────────────────────

STAMP_TYPES = [
    ('login',     '🌟', 'ログインした'),
    ('record',    '📒', 'きろくした'),
    ('quiz',      '🎓', 'クイズをといた'),
    ('read',      '📖', 'ほんをよんだ'),
    ('emotion',   '😊', 'きもちをえらんだ'),
    ('challenge', '🏆', 'チャレンジした'),
]


class StampEntry(models.Model):
    """スタンプエントリ（子どもが集めるスタンプ）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stamps')
    stamp_type = models.CharField('スタンプ種別', max_length=20)
    stamp_emoji = models.CharField('絵文字', max_length=10, default='⭐')
    note = models.CharField('メモ', max_length=100, blank=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-earned_at']


# ─── 得意なことノート（子ども向け） ────────────────────────────────────────────

class TalentNote(models.Model):
    """得意なことノート"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talent_notes')
    content = models.TextField('得意なこと・できたこと')
    emoji = models.CharField('絵文字', max_length=10, default='⭐')
    date = models.DateField('日付', auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


# ─── 模擬面接練習 ──────────────────────────────────────────────────────────────

INTERVIEW_QUESTIONS = [
    {'id': 'q1', 'question': '自己紹介をしてください', 'hint': '名前・好きなこと・やる気をつたえよう', 'emoji': '👋'},
    {'id': 'q2', 'question': 'この仕事を選んだ理由は何ですか？', 'hint': 'なぜこの仕事がしたいか話そう', 'emoji': '💼'},
    {'id': 'q3', 'question': '得意なことを教えてください', 'hint': '自分が得意なことを具体的に話そう', 'emoji': '💪'},
    {'id': 'q4', 'question': '苦手なことはありますか？どう対処しますか？', 'hint': '正直に話して、どうするか伝えよう', 'emoji': '🤔'},
    {'id': 'q5', 'question': '遅刻や欠勤について教えてください', 'hint': '時間を守ることへの意識を伝えよう', 'emoji': '⏰'},
    {'id': 'q6', 'question': 'わからないことがあったらどうしますか？', 'hint': '「聞く」「確認する」が大事だと伝えよう', 'emoji': '🙋'},
]


class InterviewPractice(models.Model):
    """模擬面接の練習回答"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_practices')
    question_id = models.CharField('質問ID', max_length=10)
    answer = models.TextField('回答')
    ai_feedback = models.TextField('AIフィードバック', blank=True)
    practiced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-practiced_at']
