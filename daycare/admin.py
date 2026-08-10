from django.contrib import admin
from .models import Child, StaffProfile, ParentProfile, StaffChildLink, ParentChildLink, SupportRecord, DevelopmentScore


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'created_at']
    search_fields = ['nickname']


@admin.register(SupportRecord)
class SupportRecordAdmin(admin.ModelAdmin):
    list_display = ['child', 'author', 'date', 'share_with_parent']
    list_filter = ['share_with_parent', 'date']
    search_fields = ['child__nickname', 'content']


@admin.register(DevelopmentScore)
class DevelopmentScoreAdmin(admin.ModelAdmin):
    list_display = ['child', 'author', 'date', 'focus', 'communication', 'social']
    list_filter = ['date']


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(StaffChildLink)
class StaffChildLinkAdmin(admin.ModelAdmin):
    list_display = ['staff', 'child']


@admin.register(ParentChildLink)
class ParentChildLinkAdmin(admin.ModelAdmin):
    list_display = ['parent', 'child']
