from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.JobTypeSelectView.as_view(), name='job_select'),
    path('<str:job_type_key>/', views.RoadmapView.as_view(), name='roadmap'),
]
