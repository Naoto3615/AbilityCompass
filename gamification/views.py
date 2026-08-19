import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import UserStreak, UserTitle, CheerMessage, WeeklyChallenge, UserChallengeProgress, InternshipRecord


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """ゲーミフィケーションダッシュボード（称号・ストリーク・ポイント）"""
    streak = UserStreak.update_streak(request.user)
    titles = UserTitle.objects.filter(user=request.user).order_by('-earned_at')
    displayed = UserTitle.objects.filter(user=request.user, is_displayed=True).first()
    point_history = request.user.point_history.all()[:10]

    # 週間チャレンジ
    from datetime import date
    week_num = date.today().isocalendar()[1] % 5 + 1  # 1〜5を循環
    try:
        challenge = WeeklyChallenge.objects.get(week_number=week_num)
        progress, _ = UserChallengeProgress.objects.get_or_create(
            user=request.user, challenge=challenge
        )
    except WeeklyChallenge.DoesNotExist:
        challenge = None
        progress = None

    return render(request, 'gamification/dashboard.html', {
        'streak': streak,
        'titles': titles,
        'displayed_title': displayed,
        'point_history': point_history,
        'challenge': challenge,
        'progress': progress,
    })


@login_required(login_url='/accounts/login/')
def title_select(request):
    """表示する称号を選択"""
    if request.method == 'POST':
        title_id = request.POST.get('title_id')
        UserTitle.objects.filter(user=request.user).update(is_displayed=False)
        if title_id:
            UserTitle.objects.filter(user=request.user, id=title_id).update(is_displayed=True)
        return redirect('gamification:dashboard')

    titles = UserTitle.objects.filter(user=request.user)
    return render(request, 'gamification/title_select.html', {'titles': titles})


@login_required(login_url='/accounts/login/')
def cheer_messages(request):
    """応援メッセージ一覧（利用者が受け取ったメッセージ）"""
    messages = CheerMessage.objects.filter(to_user=request.user)
    messages.filter(is_read=False).update(is_read=True)
    return render(request, 'gamification/cheer_messages.html', {'messages': messages})


@login_required(login_url='/accounts/login/')
def send_cheer(request):
    """支援員が応援メッセージを送る"""
    if request.method == 'POST':
        to_username = request.POST.get('to_username')
        message = request.POST.get('message', '').strip()
        emoji = request.POST.get('emoji', '💪')

        if to_username and message:
            from django.contrib.auth.models import User
            try:
                to_user = User.objects.get(username=to_username)
                CheerMessage.objects.create(
                    from_user=request.user,
                    to_user=to_user,
                    message=message,
                    emoji=emoji,
                )
            except User.DoesNotExist:
                pass
        return redirect('gamification:send_cheer')

    from accounts.models import UserProfile, SupporterProfile
    if hasattr(request.user, 'supporter_profile'):
        supported = UserProfile.objects.filter(supporter=request.user.supporter_profile)
    else:
        supported = UserProfile.objects.none()

    return render(request, 'gamification/send_cheer.html', {'supported_users': supported})


@login_required(login_url='/accounts/login/')
def internship_list(request):
    """実習記録一覧"""
    records = InternshipRecord.objects.filter(user=request.user)
    return render(request, 'gamification/internship_list.html', {'records': records})


@login_required(login_url='/accounts/login/')
def internship_add(request):
    """実習記録を追加"""
    if request.method == 'POST':
        InternshipRecord.objects.create(
            user=request.user,
            company_name=request.POST.get('company_name', ''),
            date=request.POST.get('date'),
            duration_hours=request.POST.get('duration_hours', 0),
            work_content=request.POST.get('work_content', ''),
            good_points=request.POST.get('good_points', ''),
            challenges=request.POST.get('challenges', ''),
        )
        # ポイント付与
        streak, _ = UserStreak.objects.get_or_create(user=request.user)
        streak.add_points(30, '実習記録')
        streak.total_points += 30
        streak.save()
        return redirect('gamification:internship_list')
    return render(request, 'gamification/internship_form.html')
