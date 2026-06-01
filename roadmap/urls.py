from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.CareerSelectView.as_view(), name='career_select'),
    path('<str:career_key>/', views.RoadmapView.as_view(), name='roadmap'),
]
