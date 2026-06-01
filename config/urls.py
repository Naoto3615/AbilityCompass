from django.contrib import admin
from django.urls import path, include
from django.views import View
from django.shortcuts import render
from roadmap.services import get_age_groups


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {'phases': get_age_groups()})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('diagnosis/', include('diagnosis.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('accounts/', include('accounts.urls')),
    path('daily/', include('daily.urls')),
]
