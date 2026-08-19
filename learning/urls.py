from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<str:category>/', views.quiz_play, name='quiz_play'),
    path('quiz/answer/<int:quiz_id>/', views.quiz_answer, name='quiz_answer'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('contact/', views.contact_list, name='contact_list'),
    path('contact/write/', views.contact_write, name='contact_write'),
    path('books/', views.book_list, name='book_list'),
    path('stamps/', views.stamp_rally, name='stamp_rally'),
    path('talents/', views.talent_notes, name='talent_notes'),
    path('cooldown/', views.cooldown, name='cooldown'),
    path('interview/', views.interview_practice, name='interview_practice'),
]
