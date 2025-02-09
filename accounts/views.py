from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.utils.timezone import now
from django.http import JsonResponse
from django.urls import reverse
from .models import CustomUser, GeneralUserProfile, Like
from .forms import LoginForm, AdminSettingsForm, AccountForm, AccountEditForm
from django.core.paginator import Paginator

import logging

logger = logging.getLogger(__name__)

# **管理者チェック**
def is_admin(user):
    return user.is_superuser or user.is_staff

# **ログイン機能**
def login_view(request):
    next_url = request.GET.get('next')  

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user:
                if not user.is_active:
                    messages.error(request, "このアカウントは無効化されています。")
                    return render(request, 'accounts/login.html', {'form': form})

                login(request, user)

                if next_url:
                    return redirect(next_url)

                return redirect('dashboard:admin_dashboard' if user.is_staff else 'accounts:account_list')

            else:
                messages.error(request, "ログインに失敗しました。")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# **ログアウト**
@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('accounts:login')


# **管理者設定**
@login_required
@user_passes_test(is_admin)
def admin_settings(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('accounts:settings_complete', id=user.id)

    else:
        form = AdminSettingsForm(instance=user)

    return render(request, 'accounts/admin_settings.html', {'form': form, 'user': user})


# **設定変更完了画面**
@login_required
def settings_complete(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, 'accounts/settings_complete.html', {'user': request.user})


# **アカウント一覧**
@login_required
@user_passes_test(is_admin)
def account_list(request):
    users = CustomUser.objects.filter(is_deleted=False).order_by("-id")  # ID順にソート
    paginator = Paginator(users, 5)  # 5件ごとにページネーション
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/account_list.html", {"page_obj": page_obj})

# **一般アカウント一覧**
@login_required
def general_account_list(request):
    profiles = GeneralUserProfile.objects.all()
    return render(request, 'accounts/general_account_list.html', {'profiles': profiles})

# **アカウント詳細**
def general_account_detail(request, id):
    """一般ユーザーのアカウント詳細を表示"""
    profile = get_object_or_404(GeneralUserProfile, user_id= id)
    return render(request, 'accounts/general_account_detail.html', {'profile': profile})

# **アカウント削除（論理削除）**
@login_required
def account_delete(request, id):
    """ アカウントの論理削除（Ajax対応） """
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=id)
            user.is_deleted = True  # 論理削除フラグを設定
            user.is_active = False  # 無効化
            user.save()
            return JsonResponse({"success": True, "message": "アカウントを削除しました。", "user_id": id})
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "アカウントが見つかりません。"}, status=404)
    return JsonResponse({"success": False, "message": "無効なリクエストです。"}, status=400)

# **削除済みアカウント一覧**
@login_required
@user_passes_test(is_admin)
def account_delete_list(request):
    deleted_accounts = CustomUser.objects.filter(is_deleted=True)
    return render(request, 'accounts/account_delete_list.html', {'accounts': deleted_accounts})


# **完全削除**
@login_required
@user_passes_test(is_admin)
def account_delete_permanently(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                GeneralUserProfile.objects.filter(user=user).delete()
                Like.objects.filter(user=user).delete()
                Like.objects.filter(liked_user=user).delete()

                user.delete()
                return JsonResponse({'success': True, 'message': f"アカウント {user.email} を完全に削除しました。"})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"削除に失敗しました: {str(e)}"})

    return JsonResponse({'success': False, 'message': "不正なリクエストです。"}, status=400)


# **アカウント復元**
@login_required
@user_passes_test(is_admin)
def account_restore(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.is_deleted = False
        user.save()
        messages.success(request, "アカウントを復元しました。")
    return redirect('accounts:account_delete_list')


# **アカウント作成**
@login_required
@user_passes_test(is_admin)
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account_type = form.cleaned_data.get('account_type')
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('name')
            if account_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            GeneralUserProfile.objects.create(user=user, likes_count=0)
            messages.success(request, "アカウントが作成されました。")
            return redirect('accounts:account_list')

    else:
        form = AccountForm()

    return render(request, 'accounts/account_create.html', {'form': form})


# **アカウント編集**
@login_required
@user_passes_test(is_admin)
def account_edit(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = AccountEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.is_active = form.cleaned_data.get('is_active') == 'True'
            user.save()
            messages.success(request, "アカウント情報を更新しました。")
            return redirect('accounts:account_list')

    else:
        form = AccountEditForm(instance=user)

    return render(request, 'accounts/account_edit.html', {'form': form, 'user': user})


# **ステータス切り替え**
@login_required
@user_passes_test(is_admin)
def toggle_status(request, id):
    """ステータス切り替え処理"""
    if request.method == "POST":
        user = get_object_or_404(CustomUser, id=id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({
            "success": True,
            "is_active": user.is_active,
            "message": f"ユーザー {user.name} のステータスを {'有効' if user.is_active else '無効'} に変更しました。"
        })
    return JsonResponse({"success": False, "message": "無効なリクエスト"}, status=400)

@login_required
def like_toggle(request, id):
    """いいねのトグル"""
    if request.method == 'POST':
        profile = get_object_or_404(GeneralUserProfile, id=id)

        if request.session.get(f'liked_{id}', False):
            profile.likes_count -= 1
            request.session[f'liked_{id}'] = False
        else:
            profile.likes_count += 1
            request.session[f'liked_{id}'] = True

        profile.save()
        return JsonResponse({'success': True, 'likes': profile.likes_count})

    return JsonResponse({'success': False, 'error': '無効なリクエスト'}, status=400)


# **月間いいねランキング**
@login_required
def monthly_like_ranking(request):
    """月間のいいねランキングを取得"""
    current_year = now().year
    current_month = now().month

    profiles = GeneralUserProfile.objects.annotate(
        total_likes=Count("user__likes_received", filter=Q(user__likes_received__created_at__year=current_year, user__likes_received__created_at__month=current_month))
    ).order_by("-total_likes")

    return render(request, 'accounts/monthly_like_ranking.html', {'profiles': profiles})

@login_required
def yearly_like_ranking(request):
    """年間のいいねランキングを取得"""
    current_year = now().year

    ranking = Like.objects.filter(
        created_at__year=current_year
    ).values('liked_user__id', 'liked_user__name').annotate(like_count=Count('id')).order_by('-like_count')

    return render(request, 'accounts/yearly_like_ranking.html', {'ranking': ranking})