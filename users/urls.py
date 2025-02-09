from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('settings/', views.users_settings, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
