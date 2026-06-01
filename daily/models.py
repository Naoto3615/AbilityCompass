from django.db import models
from django.utils import timezone
from accounts.models import ChildProfile

EMOTION_CHOICES = [
    (1, '😢 とてもつらい'),
    (2, '😟 すこしつらい'),
    (3, '😐 ふつう'),
    (4, '😊 まあまあ'),
    (5, '😄 とてもよい'),
]

EMOTION_EMOJIS = {1: '😢', 2: '😟', 3: '😐', 4: '😊', 5: '😄'}
EMOTION_COLORS = {1: '#93c5fd', 2: '#a5b4fc', 3: '#d1d5db', 4: '#86efac', 5: '#fde68a'}
EMOTION_LABELS = {1: 'とてもつらい', 2: 'すこしつらい', 3: 'ふつう', 4: 'まあまあ', 5: 'とてもよい'}

TASK_CATEGORIES = [
    ('learning', '学習・スキル'),
    ('character', '人間性・心の成長'),
    ('habit', '日々の習慣'),
    ('social', 'コミュニケーション'),
    ('strength', '強みを活かす活動'),
]

TASK_CATEGORY_EMOJIS = {
    'learning': '📖',
    'character': '💗',
    'habit': '⭐',
    'social': '🤝',
    'strength': '🚀',
}


class DailyTask(models.Model):
    profile = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='daily_tasks')
    date = models.DateField(default=timezone.localdate)
    category = models.CharField(max_length=20, choices=TASK_CATEGORIES)
    content = models.TextField()
    is_completed = models.BooleanField(default=False)
    points = models.IntegerField(default=10)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['category', 'id']

    def complete(self):
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()
            self.profile.total_points += self.points
            self.profile.save()
            return True
        return False

    def get_category_emoji(self):
        return TASK_CATEGORY_EMOJIS.get(self.category, '✓')

    def __str__(self):
        return f"{self.profile.nickname} / {self.date} / {self.content[:30]}"


class EmotionLog(models.Model):
    profile = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='emotion_logs')
    date = models.DateField(default=timezone.localdate)
    score = models.IntegerField(choices=EMOTION_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'date')
        ordering = ['-date']

    def get_emoji(self):
        return EMOTION_EMOJIS.get(self.score, '😐')

    def get_color(self):
        return EMOTION_COLORS.get(self.score, '#d1d5db')

    def get_label(self):
        return EMOTION_LABELS.get(self.score, 'ふつう')

    def __str__(self):
        return f"{self.profile.nickname} / {self.date} / {self.get_emoji()}"
