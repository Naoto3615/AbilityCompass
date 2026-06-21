from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('signup/supporter/', views.SupporterSignupView.as_view(), name='supporter_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.SupporterDashboardView.as_view(), name='supporter_dashboard'),
    path('avatar/', views.AvatarCreateView.as_view(), name='avatar_create'),
    path('avatar/preview/', views.AvatarPreviewView.as_view(), name='avatar_preview'),
]
