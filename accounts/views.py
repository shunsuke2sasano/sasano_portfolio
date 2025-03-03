from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.utils.timezone import now
from django.http import JsonResponse
from django.urls import reverse
from .models import CustomUser, GeneralUserProfile, Like, UserProfile
from .forms import LoginForm, AdminSettingsForm, AccountForm, AccountEditForm, UserSettingsForm, EditProfileForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

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

                if user.is_staff or user.is_superuser:
                    return redirect('dashboard:admin_dashboard')
                else:
                    return redirect('dashboard:user_dashboard')

            else:
                messages.error(request, "ログインに失敗しました。")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# **ログアウト**
@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('accounts:login_C-000')


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

# **アカウント詳細**
def general_account_detail(request, id):
    """一般ユーザーのアカウント詳細を表示"""
    profile = get_object_or_404(GeneralUserProfile, user_id= id)
    return render(request, 'accounts/general_account_detail.html', {'profile': profile})

# **アカウント削除（論理削除）**
@login_required
@login_required
def account_delete(request, user_id):
    """ アカウントの論理削除（Ajax対応） """
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            # 論理削除フラグとis_activeをFalseに
            user.is_deleted = True
            user.is_active = False
            user.save()

            # プロフィールがあれば削除、なければスキップ
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.delete()
            except UserProfile.DoesNotExist:
                pass  # スキップ

            try:
                general_user_profile = GeneralUserProfile.objects.get(user=user)
                general_user_profile.delete()
            except GeneralUserProfile.DoesNotExist:
                pass  # スキップ

            return JsonResponse({
                "success": True,
                "message": "アカウントを削除しました。",
                "user_id": user.id
            })
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
def account_delete_permanently(request, account_id):
    if request.method == "POST":
        user = get_object_or_404(CustomUser, id=account_id)
        
        if user:
            user.physical_delete() 
            return JsonResponse({"success": True, "message": f"{user.name} を完全に削除しました。"})
        else:
            return JsonResponse({"success": False, "message": "アカウントが見つかりませんでした。"})

    return JsonResponse({"success": False, "message": "不正なリクエストです。"}, status=400)
       
# **アカウント復元**
@login_required
@user_passes_test(is_admin)
def account_restore(request, id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=id)
            user.is_active = True
            user.is_deleted = False
            user.save()
            return JsonResponse({'success': True, 'message': f"{user.name} を復元しました。"})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': '無効なリクエストです。'}, status=405)

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
            else:
                user.is_staff = False
                user.is_superuser = False
            
            user.set_password(form.cleaned_data.get('password'))
            user.save()  # ここでシグナルが発火し、GeneralUserProfile が自動作成される

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
            account_type = form.cleaned_data.get('account_type')
            user = form.save(commit=False)
            if account_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.is_active = form.cleaned_data.get('is_active') == 'True'
            user.save()
            messages.success(request, "アカウント情報を更新しました。")
            return redirect('accounts:account_list')
    else:
        initial = {}
        if user.is_staff and user.is_superuser:
            initial['account_type'] = 'admin'
        else:
            initial['account_type'] = 'general'
        form = AccountEditForm(instance=user, initial=initial)
    return render(request, 'accounts/account_edit.html', {'form': form, 'user': user})


# **ステータス切り替え**
@login_required
@user_passes_test(is_admin)
@user_passes_test(lambda u: u.is_staff) 
def toggle_status(request, user_id):  # 修正: `id` → `user_id`
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({"success": True, "message": "ステータスを変更しました。"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "無効なリクエストです。"}, status=400)
    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def like_toggle(request, id):
    # 未ログインなら403 + JSON返却
    if not request.user.is_authenticated:
        login_url = reverse('accounts:login_C-000')  # ログイン画面のURL
        return JsonResponse({
            'success': False,
            'redirect': login_url,
            'message': 'ログインが必要です。'
        }, status=403)

    profile = get_object_or_404(GeneralUserProfile, id=id)
    target_user = profile.user
    current_user = request.user

    like_obj = Like.objects.filter(user=current_user, liked_user=target_user).first()
    if like_obj:
        like_obj.delete()
        liked = False
    else:
        Like.objects.create(user=current_user, liked_user=target_user)
        liked = True

    new_count = Like.objects.filter(liked_user=target_user).count()
    profile.likes_count = new_count
    profile.save()

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes': new_count
    })

# **月間いいねランキング**
def monthly_like_ranking(request):
    """月間のいいねランキングを取得"""
    current_year = now().year
    current_month = now().month

    profiles = GeneralUserProfile.objects.filter(
        user__is_active=True,
        user__is_deleted=False,
        user__is_staff=False,       # 管理者でない
        user__is_superuser=False    # スーパーユーザーでない
    ).annotate(
        total_likes=Count(
            "user__likes_received_records",
            filter=Q(
                user__likes_received_records__created_at__year=current_year,
                user__likes_received_records__created_at__month=current_month
            )
        )
    ).order_by("-total_likes")

    return render(request, 'accounts/monthly_like_ranking.html', {'profiles': profiles})

@login_required
def yearly_like_ranking(request):
    """年間のいいねランキングを取得"""
    current_year = now().year

    ranking = Like.objects.filter(
        created_at__year=current_year,
        liked_user__is_staff=False,      # 管理者でない
        liked_user__is_superuser=False   # スーパーユーザーでない
    ).values('liked_user__id', 'liked_user__name').annotate(like_count=Count('id')).order_by('-like_count')

    return render(request, 'accounts/yearly_like_ranking.html', {'ranking': ranking})

@login_required
def user_settings_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            if form.cleaned_data.get('new_password'):
                user.set_password(form.cleaned_data['new_password'])  # パスワードを変更
                update_session_auth_hash(request, user)  
            user.save()
            messages.success(request, "設定が更新されました。")
            return redirect('dashboard:user_dashboard')  # 更新後に同じページへリダイレクト
    else:
        form = UserSettingsForm(instance=user)

    return render(request, 'accounts/user_settings.html', {'form': form})


@login_required
def edit_profile(request):
    """一般ユーザーのプロフィール編集"""
    profile, created = GeneralUserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:edit_profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, "accounts/edit_profile.html", {"form": form})