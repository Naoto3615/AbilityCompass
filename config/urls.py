from django.contrib import admin
from django.urls import path, include
from django.views import View
from django.shortcuts import render, redirect


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'user_profile'):
                if request.user.user_profile.user_type == 'child':
                    return redirect('daily:child_dashboard')
                return redirect('daily:dashboard')
            elif hasattr(request.user, 'staff_profile'):
                return redirect('daycare:staff_dashboard')
            elif hasattr(request.user, 'parent_profile'):
                return redirect('daycare:parent_dashboard')
        return render(request, 'home.html')


def toggle_text_mode(request):
    current = request.session.get('text_mode', 'hiragana')
    request.session['text_mode'] = 'kanji' if current == 'hiragana' else 'hiragana'
    return redirect(request.META.get('HTTP_REFERER', '/'))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('toggle-text-mode/', toggle_text_mode, name='toggle_text_mode'),
    path('diagnosis/', include('diagnosis.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('accounts/', include('accounts.urls')),
    path('daily/', include('daily.urls')),
    path('daycare/', include('daycare.urls')),
    path('rag/', include('rag.urls')),
]
