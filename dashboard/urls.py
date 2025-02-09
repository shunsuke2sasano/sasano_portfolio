from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'dashboard'

urlpatterns = [
   path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_dashboard, name='user_dashboard'),
]
