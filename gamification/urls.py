from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('titles/', views.title_select, name='title_select'),
    path('cheer/', views.cheer_messages, name='cheer_messages'),
    path('cheer/send/', views.send_cheer, name='send_cheer'),
    path('internship/', views.internship_list, name='internship_list'),
    path('internship/add/', views.internship_add, name='internship_add'),
]
