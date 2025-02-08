from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login_C-000'),              # ログイン画面
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin/<int:id>/settings/', views.admin_settings, name='admin_settings'),  # 管理者設定画面
    path('admin/settings/complete/<int:id>/', views.settings_complete, name='settings_complete'),
    path('account_list/', views.account_list, name='account_list'),  # アカウント一覧
    path('account_create/', views.account_create, name='account_create'),  # アカウント作成
    path('account_delete_list/', views.account_delete_list, name='account_delete_list'),  # 削除済みアカウント一覧
    path('account_delete/<int:id>/', views.account_delete, name='account_delete'),  # ソフトデリート
    path('account_restore/<int:id>/', views.account_restore, name='account_restore'),  # アカウント復旧
    path('account_delete_permanently/<int:id>/', views.account_delete_permanently, name='account_delete_permanently'),   # 完全削除
    path('toggle_status/<int:id>/', views.toggle_status, name='toggle_status'),  # ステータス切り替え
    path('general_accounts/', views.general_account_list, name='general_account_list'), #一般
    path('general_accounts/<int:user_id>/', views.general_account_detail, name='general_account_detail'), #アカウント詳細
    path('like_toggle/', views.like_toggle, name='like_toggle'), #いいね機能
    path('monthly_ranking/', views.monthly_like_ranking, name='monthly_like_ranking'), #月のいいねランキング

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
