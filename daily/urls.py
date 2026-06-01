from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('task/<int:task_id>/complete/', views.CompleteTaskView.as_view(), name='complete_task'),
    path('emotion/', views.EmotionLogView.as_view(), name='emotion_log'),
]
