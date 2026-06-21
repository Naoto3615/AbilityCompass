from django.db import models
from django.contrib.auth.models import User
import json


STEP_CHOICES = [
    (1, 'ステップ1：生活習慣・基礎スキル'),
    (2, 'ステップ2：作業スキル'),
    (3, 'ステップ3：就労準備'),
]

JOB_TYPE_CHOICES = [
    ('agriculture', '🌱 農業・園芸系'),
    ('manufacturing', '🔧 製造・組み立て系'),
    ('cleaning', '🧹 清掃・環境整備系'),
    ('food_processing', '🍱 食品加工系'),
    ('service', '🛒 接客・販売補助系'),
]


class GrowthStep(models.Model):
    """就労ステップごとのタスク"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='growth_steps', null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    step_number = models.IntegerField('ステップ番号', choices=STEP_CHOICES)
    job_type = models.CharField('仕事タイプ', max_length=30, choices=JOB_TYPE_CHOICES, blank=True)
    category = models.CharField('カテゴリ', max_length=50)
    content = models.TextField('タスク内容')
    daily_action = models.TextField('今日できる小さな行動', blank=True)
    is_completed = models.BooleanField('完了', default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_number', 'id']

    def complete(self):
        if not self.is_completed:
            from django.utils import timezone
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()
            return True
        return False

    def __str__(self):
        return f"Step{self.step_number} / {self.content[:30]}"


class RoadmapCache(models.Model):
    """AI生成ロードマップのキャッシュ"""
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_type',)

    def get_content(self):
        return json.loads(self.content)

    def __str__(self):
        return f"Roadmap: {self.job_type}"
