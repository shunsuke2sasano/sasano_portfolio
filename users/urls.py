from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.users_dashboard, name='dashboard'),
    path('settings/', views.users_settings, name='settings'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
