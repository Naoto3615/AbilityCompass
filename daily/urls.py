from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('child/', views.child_dashboard, name='child_dashboard'),
    path('record/', views.DailyRecordView.as_view(), name='record'),
    path('chat/', views.AvatarChatView.as_view(), name='avatar_chat'),
    path('chat/clear/', views.AvatarChatClearView.as_view(), name='avatar_chat_clear'),
]
