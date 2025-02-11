from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('settings/', views.users_settings, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('inquiry/create/', views.inquiry_create, name='inquiry_create'), 

    # 公開ユーザー関連
    path('general_accounts/', views.general_account_list, name='general_account_list'), #公開アカウント一覧
    path('general_accounts/<int:id>/', views.general_account_detail, name='general_account_detail'), #公開アカウント詳細
]
