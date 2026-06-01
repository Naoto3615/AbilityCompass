import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import DailyTask, EmotionLog, EMOTION_EMOJIS, EMOTION_LABELS, EMOTION_COLORS, TASK_CATEGORY_EMOJIS
from .services import generate_daily_tasks, check_and_award_badges
from accounts.models import BADGE_DEFINITIONS


LOGIN_URL = '/accounts/login/'


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class DashboardView(View):
    def get(self, request):
        if not hasattr(request.user, 'child_profile'):
            return redirect('/')

        profile = request.user.child_profile
        today = timezone.localdate()

        tasks = generate_daily_tasks(profile)
        today_emotion = EmotionLog.objects.filter(profile=profile, date=today).first()

        completed_today = sum(1 for t in tasks if t.is_completed)
        total_today = len(tasks)
        progress_pct = round(completed_today / total_today * 100) if total_today else 0

        week_tasks = DailyTask.objects.filter(
            profile=profile,
            date__gte=today - timedelta(days=6)
        ).order_by('date')

        week_data = []
        for i in range(7):
            d = today - timedelta(days=6 - i)
            day_tasks = [t for t in week_tasks if t.date == d]
            done = sum(1 for t in day_tasks if t.is_completed)
            week_data.append({
                'label': ['月', '火', '水', '木', '金', '土', '日'][(d.weekday())],
                'date': d.strftime('%m/%d'),
                'done': done,
                'total': len(day_tasks),
                'is_today': d == today,
            })

        level_num, level_name, level_emoji = profile.get_level()
        next_level_points = [50, 150, 350, 700, 99999][min(level_num - 1, 4)]
        prev_level_points = [0, 50, 150, 350, 700][min(level_num - 1, 4)]
        level_progress = 0
        if next_level_points > prev_level_points:
            level_progress = round(
                (profile.total_points - prev_level_points) /
                (next_level_points - prev_level_points) * 100
            )

        badges = [BADGE_DEFINITIONS.get(b, {}) for b in profile.get_badges()]

        context = {
            'profile': profile,
            'tasks': tasks,
            'today': today,
            'today_emotion': today_emotion,
            'completed_today': completed_today,
            'total_today': total_today,
            'progress_pct': progress_pct,
            'week_data': week_data,
            'level_num': level_num,
            'level_name': level_name,
            'level_emoji': level_emoji,
            'level_progress': level_progress,
            'next_level_points': next_level_points,
            'badges': badges,
            'category_emojis': TASK_CATEGORY_EMOJIS,
        }
        return render(request, 'daily/dashboard.html', context)


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class CompleteTaskView(View):
    def post(self, request, task_id):
        if not hasattr(request.user, 'child_profile'):
            return JsonResponse({'ok': False}, status=403)

        profile = request.user.child_profile
        task = get_object_or_404(DailyTask, id=task_id, profile=profile)

        newly_completed = task.complete()
        new_badges = check_and_award_badges(profile) if newly_completed else []

        profile.refresh_from_db()
        level_num, level_name, level_emoji = profile.get_level()

        return JsonResponse({
            'ok': True,
            'newly_completed': newly_completed,
            'total_points': profile.total_points,
            'level_num': level_num,
            'level_name': level_name,
            'level_emoji': level_emoji,
            'new_badges': new_badges,
        })


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class EmotionLogView(View):
    def get(self, request):
        if not hasattr(request.user, 'child_profile'):
            return redirect('/')

        profile = request.user.child_profile
        today = timezone.localdate()
        today_log = EmotionLog.objects.filter(profile=profile, date=today).first()

        past_logs = EmotionLog.objects.filter(
            profile=profile,
            date__gte=today - timedelta(days=13)
        ).order_by('date')

        emotion_options = [
            {'score': score, 'emoji': EMOTION_EMOJIS[score], 'label': EMOTION_LABELS[score], 'color': EMOTION_COLORS[score]}
            for score in range(1, 6)
        ]

        trend_data = [
            {
                'date': log.date.strftime('%m/%d'),
                'score': log.score,
                'emoji': log.get_emoji(),
                'color': log.get_color(),
                'label': log.get_label(),
            }
            for log in past_logs
        ]

        context = {
            'profile': profile,
            'today': today,
            'today_log': today_log,
            'emotion_options': emotion_options,
            'trend_data': trend_data,
            'trend_json': json.dumps(trend_data, ensure_ascii=False),
        }
        return render(request, 'daily/emotion_log.html', context)

    def post(self, request):
        if not hasattr(request.user, 'child_profile'):
            return redirect('/')

        profile = request.user.child_profile
        today = timezone.localdate()
        score = int(request.POST.get('score', 3))
        note = request.POST.get('note', '').strip()

        log, created = EmotionLog.objects.update_or_create(
            profile=profile,
            date=today,
            defaults={'score': score, 'note': note},
        )

        check_and_award_badges(profile)
        return redirect('daily:emotion_log')
