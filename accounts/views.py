from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import login, get_user_model, authenticate, logout
from .forms import LoginForm
from django.contrib import messages
from .forms import AdminSettingsForm, AccountForm, AccountEditForm
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GeneralUserProfile, Like
from django.db.models import Count
from django.utils.timezone import now
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth import logout
from django.db import transaction
import logging
from django.urls import reverse

User = get_user_model()

# 管理者専用アクセスのチェック
def admin_check(user):
    return user.is_superuser

logger = logging.getLogger(__name__)
#ログイン機能
def login_view(request):
    next_url = request.GET.get('next')  # `next` パラメータを取得
    logger.info(f"Received next_url: {next_url}")  # デバッグ用ログ

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)

            if user:
                 
                if not user.is_active:
                    logger.warning(f"Login attempt for inactive user: {email}")
                    messages.error(request, "このアカウントは無効化されています。")
                    return render(request, 'accounts/login.html', {'form': form})

                login(request, user)
                logger.info(f"User {email} logged in successfully.")

                # `next` の値が適切に取得できているか確認
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
                    logger.info(f"Redirecting to next_url: {next_url}")
                    return redirect(next_url)

                # `next` がない場合は、通常のリダイレクト処理
                if user.is_staff or user.is_superuser:
                    return redirect('dashboard:admin_dashboard')
                else:
                    return redirect('accounts:account_list')  # 修正ポイント

            else:
                logger.warning(f"Login failed for email: {email if email else 'Unknown'}")
                messages.error(request, "ログインに失敗しました。")
        else:
            logger.warning(f"Login failed due to invalid form input. Errors: {form.errors}")
            messages.error(request, "ログインに失敗しました。入力を確認してください。")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました")
    return redirect('accounts:login')

@login_required
@user_passes_test(admin_check)  # 管理者のみアクセス許可
def admin_settings(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=user)
        if form.is_valid():
            # 保存処理
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.save()

            return redirect('accounts:settings_complete', id=user.id)
        
        else:
            print('フォームのエラー:',form.errors)
            
    else:
        form = AdminSettingsForm(instance=user)

    return render(request, 'accounts/admin_settings.html', {'form': form, 'user': user})

def settings_complete(request, id):
    """
    設定変更完了画面
    """
    user = get_object_or_404(CustomUser, id=id)
    return render(request, 'accounts/settings_complete.html', {'user': request.user})


@login_required
@user_passes_test(admin_check)
def account_list(request):
    accounts = User.objects.filter(is_deleted=False)
    paginator = Paginator(accounts, 5)  # 1ページあたり5件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/account_list.html', {'page_obj': page_obj})

@login_required
@user_passes_test(admin_check)
def account_delete(request, id, permanent=False):
    """
    アカウント削除ビュー (論理削除):
    - 論理削除 (is_deleted=True)
    """
    account = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        if not account.is_deleted:
            account.is_deleted = True
            account.save()
            messages.success(request, "アカウントを削除しました。")
        else:
            messages.error(request, "このアカウントはすでに削除されています。")
        return redirect('accounts:account_list')

    return render(request, 'accounts/confirm_delete.html', {'account': account})

@login_required
@user_passes_test(admin_check)
def toggle_status(request, id):
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({
                "success": True,
                "is_active": user.is_active,
                "message": f"アカウントが{'有効化' if user.is_active else '無効化'}されました。",
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "無効なリクエストです。"}, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account_type = form.cleaned_data.get('account_type')
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('name')  # name フィールドを username に設定
            if account_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            GeneralUserProfile.objects.create(user=user, likes_count=0)
            messages.success(request, "アカウントが作成されました。")
            return redirect('accounts:account_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = AccountForm()

    return render(request, 'accounts/account_create.html', {'form': form})


@login_required
@user_passes_test(admin_check)
def account_delete_list(request):
    deleted_accounts = User.objects.filter(is_deleted=True)  # 論理削除されたアカウント
    return render(request, 'accounts/account_delete_list.html', {'accounts': deleted_accounts})

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(admin_check)
def account_delete_permanently(request, id):
    logger.info(f"完全削除リクエスト受診: user_id={id}")
    
    user = get_object_or_404(CustomUser, id=id)
    logger.info(f"削除対象のユーザー取得成功: user_id={user.id}")

    if request.method == 'POST':
        try:
            with transaction.atomic():
                logger.info(f"削除処理開始: user_id={user.id}")
                
                # 関連データ削除
                deleted_profiles = GeneralUserProfile.objects.filter(user=user).delete()
                deleted_likes_user = Like.objects.filter(user=user).delete()
                deleted_likes_liked = Like.objects.filter(liked_user=user).delete()

                logger.info(f"GeneralUserProfile削除数: {deleted_profiles}")
                logger.info(f"Like（userとしてのいいね）削除数: {deleted_likes_user}")
                logger.info(f"Like（liked_userとしてのいいね）削除数: {deleted_likes_liked}")

                # `delete()` の呼び出しを修正
                user.delete()
                
                logger.info(f"アカウント削除完了: user_id={user.id}")
                messages.success(request, f"アカウント {user.email} を完全に削除しました。")
        except Exception as e:
            logger.error(f"削除エラー: {str(e)}")
            messages.error(request, f"削除に失敗しました: {str(e)}")

        return redirect('accounts:account_delete_list')

    logger.warning(f"無効なリクエスト（POST以外）: user_id={user.id}")
    return redirect('accounts:account_delete_list')

@login_required
@user_passes_test(admin_check)
def account_restore(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        user.is_deleted = False  # 復元
        user.save()
        messages.success(request, "アカウントを復元しました。")
        return redirect('accounts:account_delete_list')
    return redirect('accounts:account_delete_list')

def general_account_list(request):
    profiles = GeneralUserProfile.objects.all()
    logger.debug(f"取得したプロフィール: {profiles}") 
    logger.debug(f"Profiles passed to template: {profiles}")
    return render(request, 'accounts/general_account_list.html', {'profiles': profiles})

@csrf_exempt
def like_toggle(request, user_id):
    """
    いいねボタンの状態をトグルするビュー
    """
    if request.method == 'POST':
        try:
            # 該当ユーザーのプロフィールを取得
            profile = get_object_or_404(GeneralUserProfile, user_id=user_id)

            # 現在の状態をトグル
            if request.session.get(f'liked_{user_id}', False):
                profile.likes_count -= 1  # いいねを解除
                request.session[f'liked_{user_id}'] = False
            else:
                profile.likes_count += 1  # いいねを追加
                request.session[f'liked_{user_id}'] = True

            # プロフィールを保存
            profile.save()

            return JsonResponse({'success': True, 'likes': profile.likes_count})
        except GeneralUserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def monthly_like_ranking(request):
    current_month = now().month

    # 修正後のクエリ
    profiles = GeneralUserProfile.objects.filter(
        user__liked_user__created_at__month=current_month
    ).annotate(total_likes=Count('user__liked_user')).order_by('-total_likes')[:10]

    return render(request, 'accounts/monthly_like_ranking.html', {'profiles': profiles})

def general_account_detail(request, user_id):
    profile = get_object_or_404(GeneralUserProfile, user_id=user_id)
    return render(request, 'accounts/general_account_detail.html', {'profile': profile})

def custom_logout_view(request):
    logout(request)
    return redirect('http://localhost:8000/accounts/login/') 

@login_required
@user_passes_test(admin_check)  # 管理者のみアクセス可能
def account_edit(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = AccountEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))  # パスワード変更があれば更新
            user.is_active = form.cleaned_data.get('is_active') == 'True'
            user.save()
            messages.success(request, "アカウント情報を更新しました。")
            return redirect('accounts:account_list')

        messages.error(request, "入力にエラーがあります。")

    else:
        form = AccountEditForm(instance=user)

    return render(request, 'accounts/account_edit.html', {'form': form, 'user': user})
