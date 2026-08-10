from django.contrib import admin
from .models import SupportRecordEmbedding, UserProfileEmbedding


@admin.register(SupportRecordEmbedding)
class SupportRecordEmbeddingAdmin(admin.ModelAdmin):
    list_display = ['support_record', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserProfileEmbedding)
class UserProfileEmbeddingAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
