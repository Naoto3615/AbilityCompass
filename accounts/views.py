from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .forms import UserSignupForm, SupporterSignupForm
from .models import SupporterProfile, SupporterNote, UserProfile, DEFAULT_AVATAR_CONFIG


class UserSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('daily:dashboard')
        text_mode = request.session.get('text_mode', 'hiragana')
        return render(request, 'accounts/user_signup.html', {'form': UserSignupForm(text_mode=text_mode)})

    def post(self, request):
        text_mode = request.session.get('text_mode', 'hiragana')
        form = UserSignupForm(request.POST, text_mode=text_mode)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('daily:dashboard')
        return render(request, 'accounts/user_signup.html', {'form': form})


class SupporterSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:supporter_dashboard')
        text_mode = request.session.get('text_mode', 'hiragana')
        return render(request, 'accounts/supporter_signup.html', {'form': SupporterSignupForm(text_mode=text_mode)})

    def post(self, request):
        text_mode = request.session.get('text_mode', 'hiragana')
        form = SupporterSignupForm(request.POST, text_mode=text_mode)
        if form.is_valid():
            user = form.save()
            supporter_profile = SupporterProfile.objects.create(user=user)

            target_username = form.cleaned_data.get('target_username', '').strip()
            if target_username:
                from django.contrib.auth.models import User as DjangoUser
                try:
                    target_user = DjangoUser.objects.get(username=target_username)
                    if hasattr(target_user, 'user_profile'):
                        target_user.user_profile.supporter = supporter_profile
                        target_user.user_profile.save()
                except DjangoUser.DoesNotExist:
                    pass

            login(request, user)
            return redirect('accounts:supporter_dashboard')
        return render(request, 'accounts/supporter_signup.html', {'form': form})


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
        text_mode = request.session.get('text_mode', 'hiragana')
        error = 'IDまたはパスワードが　ちがいます' if text_mode == 'kanji' else 'IDか ぱすわーどが ちがいます'
        return render(request, 'accounts/login.html', {'error': error})

    def _redirect_by_role(self, user):
        if hasattr(user, 'user_profile'):
            return redirect('daily:dashboard')
        elif hasattr(user, 'supporter_profile'):
            return redirect('accounts:supporter_dashboard')
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


# ─── アバター作成 ─────────────────────────────────────────────────────────────

SKIN_OPTIONS = [
    {'value': 'light',  'color': '#FFDAB9', 'label': 'ライト'},
    {'value': 'medium', 'color': '#D2956C', 'label': 'ミディアム'},
    {'value': 'dark',   'color': '#8B4513', 'label': 'ダーク'},
]

HAIR_STYLE_OPTIONS = [
    {'value': 'short', 'emoji': '🙂', 'label': 'ショート'},
    {'value': 'long',  'emoji': '👩', 'label': 'ロング'},
    {'value': 'curly', 'emoji': '🌀', 'label': 'くるくる'},
    {'value': 'none',  'emoji': '😐', 'label': 'なし'},
]

HAIR_COLOR_OPTIONS = [
    {'value': 'black',  'color': '#1a1a1a', 'label': 'くろ'},
    {'value': 'brown',  'color': '#8B4513', 'label': 'ちゃいろ'},
    {'value': 'blonde', 'color': '#FFD700', 'label': 'きいろ'},
    {'value': 'gray',   'color': '#808080', 'label': 'グレー'},
]

EYE_OPTIONS = [
    {'value': 'normal', 'emoji': '👀', 'label': 'ふつう'},
    {'value': 'round',  'emoji': '😮', 'label': 'まるい'},
    {'value': 'happy',  'emoji': '😊', 'label': 'わらい'},
]

EXPRESSION_OPTIONS = [
    {'value': 'happy',   'emoji': '😊', 'label': 'えがお'},
    {'value': 'normal',  'emoji': '😐', 'label': 'ふつう'},
    {'value': 'worried', 'emoji': '😟', 'label': 'しんぱい'},
]

ACCESSORY_OPTIONS = [
    {'value': 'none',    'emoji': '❌', 'label': 'なし'},
    {'value': 'glasses', 'emoji': '👓', 'label': 'めがね'},
]


def _build_config_from_post(post_data, base_config):
    """POSTデータからアバター設定を構築する（既存設定のjob_outfitなどは保持）。"""
    config = dict(base_config)
    for key in ('skin', 'hair_style', 'hair_color', 'eye_type', 'expression', 'accessory'):
        if key in post_data:
            config[key] = post_data[key]
    return config


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AvatarCreateView(View):
    def get(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')
        profile = request.user.user_profile
        config = profile.get_avatar_config()
        return render(request, 'accounts/avatar_create.html', {
            'config': config,
            'skin_options': SKIN_OPTIONS,
            'hair_style_options': HAIR_STYLE_OPTIONS,
            'hair_color_options': HAIR_COLOR_OPTIONS,
            'eye_options': EYE_OPTIONS,
            'expression_options': EXPRESSION_OPTIONS,
            'accessory_options': ACCESSORY_OPTIONS,
        })

    def post(self, request):
        if not hasattr(request.user, 'user_profile'):
            return redirect('/')
        profile = request.user.user_profile
        base = profile.get_avatar_config()
        new_config = _build_config_from_post(request.POST, base)
        profile.avatar_config = new_config
        profile.save()
        return redirect('daily:dashboard')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AvatarPreviewView(View):
    """JSからのAJAXリクエストでSVGプレビューを返す。"""
    def get(self, request):
        if not hasattr(request.user, 'user_profile'):
            return HttpResponse('')
        profile = request.user.user_profile
        base = profile.get_avatar_config()
        config = _build_config_from_post(request.GET, base)

        from django.template.loader import render_to_string
        from diagnosis.templatetags.text_mode import (
            SKIN_COLORS, HAIR_COLORS, DEFAULT_AVATAR_CONFIG,
        )
        cfg = dict(DEFAULT_AVATAR_CONFIG)
        cfg.update(config)
        skin_color = SKIN_COLORS.get(cfg['skin'], SKIN_COLORS['light'])
        hair_color = HAIR_COLORS.get(cfg['hair_color'], HAIR_COLORS['black'])
        svg = render_to_string('components/avatar.html', {
            'cfg': cfg,
            'size': 140,
            'skin_color': skin_color,
            'hair_color': hair_color,
        })
        return HttpResponse(svg, content_type='text/html')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class SupporterDashboardView(View):
    def get(self, request):
        if not hasattr(request.user, 'supporter_profile'):
            return redirect('/')

        from django.utils import timezone
        from datetime import timedelta
        from daily.models import DailyRecord
        from roadmap.services import get_supporter_advice

        supporter_profile = request.user.supporter_profile
        supported_users = UserProfile.objects.filter(supporter=supporter_profile)

        users_data = []
        for up in supported_users:
            week_ago = timezone.localdate() - timedelta(days=7)
            recent_records = list(DailyRecord.objects.filter(
                user=up.user, date__gte=week_ago
            ).order_by('date'))

            avg_emotion = None
            if recent_records:
                avg_emotion = round(sum(r.emotion_stamp for r in recent_records) / len(recent_records), 1)

            ai_advice = get_supporter_advice(up, recent_records)

            notes = SupporterNote.objects.filter(
                supporter=request.user, target_user=up.user
            ).order_by('-created_at')[:3]

            emotion_trend = [
                {
                    'date': r.date.strftime('%m/%d'),
                    'score': r.emotion_stamp,
                    'emoji': r.get_emotion_emoji(),
                    'color': r.get_emotion_color(),
                    'label': r.get_emotion_label(),
                }
                for r in recent_records
            ]

            users_data.append({
                'profile': up,
                'recent_records': recent_records[-3:],
                'avg_emotion': avg_emotion,
                'ai_advice': ai_advice,
                'notes': notes,
                'emotion_trend': emotion_trend,
            })

        context = {
            'supporter_profile': supporter_profile,
            'users_data': users_data,
        }
        return render(request, 'accounts/supporter_dashboard.html', context)

    def post(self, request):
        """支援者メモの追加"""
        if not hasattr(request.user, 'supporter_profile'):
            return redirect('/')

        target_username = request.POST.get('target_username', '')
        content = request.POST.get('content', '').strip()

        if content and target_username:
            from django.contrib.auth.models import User as DjangoUser
            try:
                target_user = DjangoUser.objects.get(username=target_username)
                SupporterNote.objects.create(
                    supporter=request.user,
                    target_user=target_user,
                    content=content,
                )
            except DjangoUser.DoesNotExist:
                pass

        return redirect('accounts:supporter_dashboard')
