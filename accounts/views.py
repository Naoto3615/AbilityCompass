from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .forms import ChildSignupForm, ParentSignupForm
from .models import ParentProfile


class ChildSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('daily:dashboard')
        return render(request, 'accounts/child_signup.html', {'form': ChildSignupForm()})

    def post(self, request):
        form = ChildSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('daily:dashboard')
        return render(request, 'accounts/child_signup.html', {'form': form})


class ParentSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:parent_dashboard')
        return render(request, 'accounts/parent_signup.html', {'form': ParentSignupForm()})

    def post(self, request):
        form = ParentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            parent_profile = ParentProfile.objects.create(user=user)

            child_username = form.cleaned_data.get('child_username', '').strip()
            if child_username:
                from django.contrib.auth.models import User
                try:
                    child_user = User.objects.get(username=child_username)
                    if hasattr(child_user, 'child_profile'):
                        parent_profile.children.add(child_user.child_profile)
                except User.DoesNotExist:
                    pass

            login(request, user)
            return redirect('accounts:parent_dashboard')
        return render(request, 'accounts/parent_signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self._redirect_by_role(request.user)
        return render(request, 'accounts/login.html', {'error': None})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next', '')
            if next_url:
                return redirect(next_url)
            return self._redirect_by_role(user)
        return render(request, 'accounts/login.html', {'error': 'IDまたはパスワードが正しくありません'})

    def _redirect_by_role(self, user):
        if hasattr(user, 'child_profile'):
            return redirect('daily:dashboard')
        elif hasattr(user, 'parent_profile'):
            return redirect('accounts:parent_dashboard')
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class ParentDashboardView(View):
    def get(self, request):
        if not hasattr(request.user, 'parent_profile'):
            return redirect('/')

        from django.utils import timezone
        from datetime import timedelta
        from daily.models import DailyTask, EmotionLog
        from daily.services import get_guardian_ai_advice

        parent_profile = request.user.parent_profile
        children = parent_profile.children.all()

        children_data = []
        for child in children:
            week_ago = timezone.localdate() - timedelta(days=7)
            recent_tasks = list(DailyTask.objects.filter(profile=child, date__gte=week_ago))
            recent_emotions = list(EmotionLog.objects.filter(profile=child, date__gte=week_ago).order_by('date'))

            completed = sum(1 for t in recent_tasks if t.is_completed)
            total = len(recent_tasks)
            completion_rate = round(completed / total * 100) if total > 0 else 0

            level_num, level_name, level_emoji = child.get_level()

            ai_advice = get_guardian_ai_advice(child, recent_tasks, recent_emotions)

            emotion_trend = [
                {
                    'date': e.date.strftime('%m/%d'),
                    'score': e.score,
                    'emoji': e.get_emoji(),
                    'color': e.get_color(),
                }
                for e in recent_emotions
            ]

            children_data.append({
                'profile': child,
                'recent_tasks': recent_tasks[:5],
                'completion_rate': completion_rate,
                'completed_count': completed,
                'total_count': total,
                'level_num': level_num,
                'level_name': level_name,
                'level_emoji': level_emoji,
                'ai_advice': ai_advice,
                'emotion_trend': emotion_trend,
                'badges': [
                    __import__('accounts.models', fromlist=['BADGE_DEFINITIONS']).BADGE_DEFINITIONS.get(b, {})
                    for b in child.get_badges()
                ],
            })

        context = {
            'parent': parent_profile,
            'children_data': children_data,
        }
        return render(request, 'accounts/parent_dashboard.html', context)
