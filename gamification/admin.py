from django.contrib import admin
from .models import UserStreak, UserTitle, WeeklyChallenge, UserChallengeProgress, CheerMessage, InternshipRecord, PointHistory

admin.site.register(UserStreak)
admin.site.register(UserTitle)
admin.site.register(WeeklyChallenge)
admin.site.register(UserChallengeProgress)
admin.site.register(CheerMessage)
admin.site.register(PointHistory)

@admin.register(InternshipRecord)
class InternshipRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'date', 'duration_hours']
    list_filter = ['date']
    search_fields = ['user__username', 'company_name']
