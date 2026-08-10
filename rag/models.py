from django.db import models
import json


class SupportRecordEmbedding(models.Model):
    """支援記録のベクトル埋め込み（JSON形式、SQLite互換）"""
    support_record = models.OneToOneField(
        'daycare.SupportRecord',
        on_delete=models.CASCADE,
        related_name='embedding'
    )
    embedding_vector = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_vector(self):
        return json.loads(self.embedding_vector)

    def set_vector(self, vector):
        self.embedding_vector = json.dumps(vector)

    class Meta:
        verbose_name = '支援記録埋め込み'
        verbose_name_plural = '支援記録埋め込み一覧'


class UserProfileEmbedding(models.Model):
    """利用者プロフィール＋日常記録のベクトル埋め込み"""
    user_profile = models.OneToOneField(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='embedding'
    )
    embedding_vector = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_vector(self):
        return json.loads(self.embedding_vector)

    def set_vector(self, vector):
        self.embedding_vector = json.dumps(vector)

    class Meta:
        verbose_name = '利用者埋め込み'
        verbose_name_plural = '利用者埋め込み一覧'
