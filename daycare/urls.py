from django.urls import path
from . import views

app_name = 'daycare'

urlpatterns = [
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/signup/', views.staff_signup, name='staff_signup'),
    path('staff/children/add/', views.child_add, name='child_add'),
    path('staff/children/<int:child_id>/', views.child_detail, name='child_detail'),
    path('staff/children/<int:child_id>/record/', views.record_add, name='record_add'),
    path('staff/children/<int:child_id>/add-parent/', views.add_parent_to_child, name='add_parent_to_child'),
    path('staff/children/<int:child_id>/scores/', views.score_add, name='score_add'),
    path('children/<int:child_id>/growth/', views.child_growth, name='child_growth'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/signup/', views.parent_signup, name='parent_signup'),
]
