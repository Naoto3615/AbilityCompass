import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import DailyRecord, AvatarChatMessage, EMOTION_CHOICES, HEALTH_CHOICES, EMOTION_EMOJIS, EMOTION_COLORS, EMOTION_LABELS

LOGIN_URL = '/accounts/login/'


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class DashboardView(View):
    def get(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')

        profile = request.user.user_profile
        today = timezone.localdate()

        today_record = DailyRecord.objects.filter(user=request.user, date=today).first()

        # 過去7日間の記録
        week_ago = today - timedelta(days=6)
        week_records = DailyRecord.objects.filter(
            user=request.user, date__gte=week_ago
        ).order_by('date')

        # 週間グラフデータ
        week_data = []
        for i in range(7):
            d = week_ago + timedelta(days=i)
            rec = next((r for r in week_records if r.date == d), None)
            week_data.append({
                'label': ['月', '火', '水', '木', '金', '土', '日'][d.weekday()],
                'date': d.strftime('%m/%d'),
                'score': rec.emotion_stamp if rec else None,
                'emoji': EMOTION_EMOJIS.get(rec.emotion_stamp, '') if rec else '',
                'color': EMOTION_COLORS.get(rec.emotion_stamp, '#e5e7eb') if rec else '#e5e7eb',
                'is_today': d == today,
                'has_record': rec is not None,
            })

        # 記録日数
        record_count = week_records.count()

        # アバター設定（今日の感情ログで表情を上書き）
        avatar_config = profile.get_avatar_config()
        if today_record:
            stamp = today_record.emotion_stamp
            if stamp >= 4:
                avatar_config['expression'] = 'happy'
            elif stamp <= 2:
                avatar_config['expression'] = 'worried'
            else:
                avatar_config['expression'] = 'normal'

        # タスク完了数・ログイン連続日数でバッジを更新
        total_records = DailyRecord.objects.filter(user=request.user).count()
        avatar_config['badge_count'] = total_records

        context = {
            'profile': profile,
            'today': today,
            'today_record': today_record,
            'week_data': week_data,
            'week_data_json': json.dumps(week_data, ensure_ascii=False, default=str),
            'record_count': record_count,
            'avatar_config': avatar_config,
        }
        return render(request, 'daily/dashboard.html', context)


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class DailyRecordView(View):
    def get(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')

        today = timezone.localdate()
        today_record = DailyRecord.objects.filter(user=request.user, date=today).first()

        emotion_options = [
            {'value': score, 'label': label, 'emoji': EMOTION_EMOJIS[score], 'color': EMOTION_COLORS[score]}
            for score, label in sorted(EMOTION_CHOICES, key=lambda x: -x[0])
        ]
        health_options = [
            {'value': score, 'label': label}
            for score, label in HEALTH_CHOICES
        ]

        context = {
            'profile': request.user.user_profile,
            'today': today,
            'today_record': today_record,
            'emotion_options': emotion_options,
            'health_options': health_options,
        }
        return render(request, 'daily/record.html', context)

    def post(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')

        today = timezone.localdate()
        did_well = request.POST.get('did_well', '').strip()
        struggled_with = request.POST.get('struggled_with', '').strip()
        emotion_stamp = int(request.POST.get('emotion_stamp', 3))
        health_score = int(request.POST.get('health_score', 2))

        DailyRecord.objects.update_or_create(
            user=request.user,
            date=today,
            defaults={
                'did_well': did_well,
                'struggled_with': struggled_with,
                'emotion_stamp': emotion_stamp,
                'health_score': health_score,
            },
        )

        return redirect('daily:dashboard')


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class AvatarChatView(View):
    """アバターチャットページ"""

    def get(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')

        profile = request.user.user_profile
        messages = AvatarChatMessage.objects.filter(profile=profile).order_by('created_at')[:30]
        avatar_config = profile.get_avatar_config()
        text_mode = request.session.get('text_mode', 'hiragana')

        context = {
            'profile': profile,
            'messages': messages,
            'avatar_config': avatar_config,
            'text_mode': text_mode,
        }
        return render(request, 'daily/avatar_chat.html', context)

    def post(self, request):
        if not hasattr(request.user, 'user_profile'):
            return JsonResponse({'error': 'profile not found'}, status=400)

        profile = request.user.user_profile
        text_mode = request.session.get('text_mode', 'hiragana')

        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except (json.JSONDecodeError, AttributeError):
            user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'empty message'}, status=400)

        AvatarChatMessage.objects.create(
            profile=profile,
            role='user',
            content=user_message,
        )

        from .services import chat_with_avatar
        avatar_reply = chat_with_avatar(profile, user_message, text_mode)

        AvatarChatMessage.objects.create(
            profile=profile,
            role='avatar',
            content=avatar_reply,
        )

        return JsonResponse({'reply': avatar_reply})


@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class AvatarChatClearView(View):
    """チャット履歴をクリアする"""

    def post(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')

        profile = request.user.user_profile
        AvatarChatMessage.objects.filter(profile=profile).delete()
        return redirect('daily:avatar_chat')
