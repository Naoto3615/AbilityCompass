from django.contrib import admin
from .models import MannerQuiz, QuizChoice, UserQuizResult, DailyScheduleTemplate, ScheduleItem, ContactNote, BookRecord, StampEntry, TalentNote, InterviewPractice


class QuizChoiceInline(admin.TabularInline):
    model = QuizChoice
    extra = 4


@admin.register(MannerQuiz)
class MannerQuizAdmin(admin.ModelAdmin):
    list_display = ['category', 'question', 'order']
    list_filter = ['category']
    inlines = [QuizChoiceInline]


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 5


@admin.register(DailyScheduleTemplate)
class DailyScheduleTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'day_of_week', 'is_active']
    inlines = [ScheduleItemInline]


admin.site.register(ContactNote)
admin.site.register(BookRecord)
admin.site.register(StampEntry)
admin.site.register(TalentNote)
admin.site.register(InterviewPractice)
admin.site.register(UserQuizResult)
