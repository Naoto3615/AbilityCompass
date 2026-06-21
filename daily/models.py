from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


EMOTION_CHOICES = [
    (5, '😄 とてもよい'),
    (4, '😊 まあまあ'),
    (3, '😐 ふつう'),
    (2, '😟 すこしつらい'),
    (1, '😢 とてもつらい'),
]

HEALTH_CHOICES = [
    (3, '💪 からだがよい'),
    (2, '😌 ふつう'),
    (1, '🤒 つらい'),
]

EMOTION_EMOJIS = {5: '😄', 4: '😊', 3: '😐', 2: '😟', 1: '😢'}
EMOTION_COLORS = {5: '#fde68a', 4: '#86efac', 3: '#d1d5db', 2: '#a5b4fc', 1: '#93c5fd'}
EMOTION_LABELS = {5: 'とてもよい', 4: 'まあまあ', 3: 'ふつう', 2: 'すこしつらい', 1: 'とてもつらい'}
HEALTH_LABELS = {3: 'からだがよい', 2: 'ふつう', 1: 'つらい'}


class DailyRecord(models.Model):
    """日々の記録"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_records')
    date = models.DateField(default=timezone.localdate)
    did_well = models.TextField('できたこと', blank=True)
    struggled_with = models.TextField('むずかしかったこと', blank=True)
    emotion_stamp = models.IntegerField('きもち', choices=EMOTION_CHOICES, default=3)
    health_score = models.IntegerField('からだのようす', choices=HEALTH_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def get_emotion_emoji(self):
        return EMOTION_EMOJIS.get(self.emotion_stamp, '😐')

    def get_emotion_color(self):
        return EMOTION_COLORS.get(self.emotion_stamp, '#d1d5db')

    def get_emotion_label(self):
        return EMOTION_LABELS.get(self.emotion_stamp, 'ふつう')

    def get_health_label(self):
        return HEALTH_LABELS.get(self.health_score, 'ふつう')

    def __str__(self):
        return f"{self.user.username} / {self.date} / {self.get_emotion_emoji()}"


class AvatarChatMessage(models.Model):
    """アバターとのチャット履歴"""
    profile = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='chat_messages',
    )
    role = models.CharField(max_length=10)  # 'user' or 'avatar'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.profile.nickname} [{self.role}]: {self.content[:30]}"
