from django.urls import path
from . import views

app_name = 'rag'

urlpatterns = [
    path('staff/child/<int:child_id>/', views.rag_advice_staff, name='advice_staff'),
    path('user/', views.rag_advice_user, name='advice_user'),
    path('staff/child/<int:child_id>/embed/', views.embed_records, name='embed_records'),
]
