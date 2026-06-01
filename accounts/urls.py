from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/child/', views.ChildSignupView.as_view(), name='child_signup'),
    path('signup/parent/', views.ParentSignupView.as_view(), name='parent_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('parent/dashboard/', views.ParentDashboardView.as_view(), name='parent_dashboard'),
]
