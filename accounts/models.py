from django.db import models
from django.contrib.auth.models import User
import json


DISABILITY_LEVEL_CHOICES = [
    ('mild', '軽度'),
    ('moderate', '中度'),
    ('other', 'その他'),
]


DEFAULT_AVATAR_CONFIG = {
    "skin": "light",
    "hair_style": "short",
    "hair_color": "black",
    "eye_type": "normal",
    "accessory": "none",
    "job_outfit": "none",
    "expression": "happy",
    "badge_count": 0,
    "rosy_cheeks": False,
}


class UserProfile(models.Model):
    """就労支援利用者のプロフィール"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    nickname = models.CharField('ニックネーム', max_length=30)
    disability_level = models.CharField('障害区分', max_length=20, choices=DISABILITY_LEVEL_CHOICES, default='mild')
    avatar_emoji = models.CharField('アバター絵文字', max_length=10, default='🌟')
    avatar_config = models.JSONField('アバター設定', default=dict, blank=True)
    supporter = models.ForeignKey(
        'SupporterProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='supported_users'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_avatar_config(self):
        """デフォルト値を補完したアバター設定を返す"""
        config = dict(DEFAULT_AVATAR_CONFIG)
        config.update(self.avatar_config or {})
        return config

    def __str__(self):
        return f"{self.nickname} ({self.user.username})"


class SupporterProfile(models.Model):
    """支援者（家族・支援員）のプロフィール"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supporter_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"支援者: {self.user.username}"


class SupporterNote(models.Model):
    """支援者のメモ"""
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_written')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_received')
    content = models.TextField('メモ内容')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.supporter.username} → {self.target_user.username}: {self.content[:30]}"
