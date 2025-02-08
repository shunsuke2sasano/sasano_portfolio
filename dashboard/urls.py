
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),#管理者
    path('users/', views.user_dashboard, name='user_dashboard'),  # 新しい一般ユーザー画面
    path('users/edit_profile/', views.edit_profile, name='edit_profile'),  # プロフィール編集
    path('users/settings/', views.users_settings, name='settings'),  # 設定変更
    path('logout/', LogoutView.as_view(), name='logout'),
]
