from django.db import models
from django.contrib.auth.models import User


class UserStreak(models.Model):
    """ログインストリーク（連続ログイン日数）"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField('現在の連続日数', default=0)
    max_streak = models.IntegerField('最長連続日数', default=0)
    last_active_date = models.DateField('最後のアクティブ日', null=True, blank=True)
    total_points = models.IntegerField('累計ポイント', default=0)

    def __str__(self):
        return f"{self.user.username}: {self.current_streak}日連続"

    @classmethod
    def update_streak(cls, user):
        from django.utils import timezone
        today = timezone.localdate()
        streak, _ = cls.objects.get_or_create(user=user)

        if streak.last_active_date is None:
            streak.current_streak = 1
            streak.add_points(10, 'ログイン')
        elif streak.last_active_date == today:
            return streak  # 既に今日更新済み
        elif (today - streak.last_active_date).days == 1:
            streak.current_streak += 1
            points = 10 + (streak.current_streak * 2)  # 連続日数ボーナス
            streak.add_points(points, f'{streak.current_streak}日連続ログイン')
        else:
            streak.current_streak = 1
            streak.add_points(10, 'ログイン')

        streak.max_streak = max(streak.max_streak, streak.current_streak)
        streak.last_active_date = today
        streak.save()
        # 称号チェック
        UserTitle.check_and_award(user, streak)
        return streak

    def add_points(self, points, reason=''):
        self.total_points += points
        PointHistory.objects.create(user=self.user, points=points, reason=reason)


class PointHistory(models.Model):
    """ポイント獲得履歴"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_history')
    points = models.IntegerField('ポイント')
    reason = models.CharField('理由', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


TITLE_DEFINITIONS = [
    ('first_login',    '🌱 はじめの一歩',   'はじめてログインした',       1,   'streak'),
    ('week_streak',    '🔥 7日連続',        '7日連続でログインした',       7,   'streak'),
    ('month_streak',   '⚡ 30日連続',       '30日連続でログインした',      30,  'streak'),
    ('point_100',      '💰 ポイント100',    'ポイントを100貯めた',         100, 'points'),
    ('point_500',      '💎 ポイント500',    'ポイントを500貯めた',         500, 'points'),
    ('diagnosis_done', '🎯 診断マスター',   '診断を1回受けた',             1,   'diagnosis'),
    ('quiz_10',        '📚 クイズ達人',     'クイズを10問正解した',        10,  'quiz'),
    ('record_7',       '📒 記録の達人',     '7回記録した',                 7,   'records'),
    ('record_30',      '🏆 記録チャンピオン', '30回記録した',              30,  'records'),
]


class UserTitle(models.Model):
    """獲得した称号"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titles')
    title_key = models.CharField('称号キー', max_length=30)
    title_name = models.CharField('称号名', max_length=50)
    description = models.CharField('説明', max_length=100)
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField('表示中', default=False)

    class Meta:
        unique_together = ('user', 'title_key')

    def __str__(self):
        return f"{self.user.username}: {self.title_name}"

    @classmethod
    def check_and_award(cls, user, streak=None):
        from daily.models import DailyRecord
        from diagnosis.models import DiagnosisSession

        if streak is None:
            streak, _ = UserStreak.objects.get_or_create(user=user)

        record_count = DailyRecord.objects.filter(user=user).count()
        diagnosis_count = DiagnosisSession.objects.filter(user=user).count()
        quiz_correct = QuizResult.objects.filter(user=user, is_correct=True).count()

        for key, name, desc, threshold, ttype in TITLE_DEFINITIONS:
            if cls.objects.filter(user=user, title_key=key).exists():
                continue
            earned = False
            if ttype == 'streak' and streak.current_streak >= threshold:
                earned = True
            elif ttype == 'points' and streak.total_points >= threshold:
                earned = True
            elif ttype == 'diagnosis' and diagnosis_count >= threshold:
                earned = True
            elif ttype == 'records' and record_count >= threshold:
                earned = True
            elif ttype == 'quiz' and quiz_correct >= threshold:
                earned = True

            if earned:
                cls.objects.create(
                    user=user, title_key=key, title_name=name, description=desc
                )
                streak.add_points(50, f'称号獲得: {name}')


class WeeklyChallenge(models.Model):
    """週間チャレンジ定義"""
    title = models.CharField('タイトル', max_length=100)
    description = models.CharField('説明', max_length=200)
    emoji = models.CharField('絵文字', max_length=10, default='🎯')
    target_type = models.CharField('種類', max_length=20)  # login/record/quiz/diagnosis
    target_count = models.IntegerField('目標数', default=3)
    reward_points = models.IntegerField('報酬ポイント', default=100)
    week_number = models.IntegerField('週番号', default=1)  # 1〜52

    def __str__(self):
        return f"Week{self.week_number}: {self.title}"


class UserChallengeProgress(models.Model):
    """ユーザーのチャレンジ進捗"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_progress')
    challenge = models.ForeignKey(WeeklyChallenge, on_delete=models.CASCADE)
    progress = models.IntegerField('進捗', default=0)
    completed = models.BooleanField('完了', default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')


class QuizResult(models.Model):
    """クイズ回答結果（称号チェック用）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results_gami')
    quiz_key = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)


class CheerMessage(models.Model):
    """支援員から利用者への応援メッセージ"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cheer_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cheer_received')
    message = models.TextField('メッセージ')
    emoji = models.CharField('絵文字', max_length=10, default='💪')
    is_read = models.BooleanField('既読', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}: {self.message[:30]}"


class InternshipRecord(models.Model):
    """実習記録"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internship_records')
    company_name = models.CharField('実習先名', max_length=100)
    date = models.DateField('実習日')
    duration_hours = models.DecimalField('実習時間', max_digits=4, decimal_places=1, default=0)
    work_content = models.TextField('作業内容')
    good_points = models.TextField('良かったこと', blank=True)
    challenges = models.TextField('課題・気になったこと', blank=True)
    staff_comment = models.TextField('支援員コメント', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}: {self.company_name} ({self.date})"
