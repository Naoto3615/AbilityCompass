from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    path('', views.DiagnosisStartView.as_view(), name='start'),
    path('questions/', views.DiagnosisQuestionsView.as_view(), name='questions'),
    path('result/', views.DiagnosisResultView.as_view(), name='result'),
    path('history/', views.diagnosis_history, name='history'),
    path('careers/', views.CareerListView.as_view(), name='career_list'),
    path('careers/<str:job_type>/', views.CareerDetailView.as_view(), name='career_detail'),
]
