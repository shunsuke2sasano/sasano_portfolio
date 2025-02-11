from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import EmailUpdateForm, PasswordUpdateForm, UserProfileEditForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from users.forms import InquiryCreateForm, UserForm
from inquiry.models import Inquiry, Category
from .models import UserProfile

User = get_user_model()


@login_required
def users_settings(request):
    """
    ユーザーの設定（メールアドレス変更、パスワード変更）
    """
    if request.method == 'POST':
        email_form = EmailUpdateForm(request.POST, instance=request.user)
        password_form = PasswordUpdateForm(request.POST)

        if email_form.is_valid() and password_form.is_valid():
            email_form.save()
            request.user.set_password(password_form.cleaned_data['password'])
            request.user.save()
            messages.success(request, '設定が更新されました。')
            return redirect('dashboard:user_dashboard')  # 修正: ダッシュボードへリダイレクト
        else:
            messages.error(request, '入力内容にエラーがあります。')

    else:
        email_form = EmailUpdateForm(instance=request.user)
        password_form = PasswordUpdateForm()

    return render(request, 'users/users_settings.html', {
        'email_form': email_form,
        'password_form': password_form,
    })


@login_required
def edit_profile(request):
    """
    プロフィール編集
    """
    user = request.user
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "プロフィールが更新されました。")
            return redirect('dashboard:user_dashboard')  # 修正: ダッシュボードへ
    else:
        form = UserProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})

def inquiry_create(request):
    categories = Category.objects.filter(is_deleted=False)
    
    if request.method == "POST":
        form = InquiryCreateForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.status = 'pending'
            inquiry.save()
            messages.success(request, "お問い合わせが送信されました。")
            return redirect('users:inquiry_create')
    else:
        form = InquiryCreateForm()

    return render(request, 'users/inquiry_create.html', {'form': form, 'categories': categories})

# **一般アカウント一覧**
def general_account_list(request):
    profiles = UserProfile.objects.filter(user__is_active=True) 
    return render(request, 'users/general_account_list.html', {'profiles': profiles})

def general_account_detail(request, user_id):
    profile = UserProfile.objects.get(user_id=user_id)
    return render(request, 'users/general_account_detail.html', {'profile': profile})

# users/views.py
def general_account_list(request):
    profiles = UserProfile.objects.filter(user__is_active=True)  # 追加: アクティブなユーザーのみ
    return render(request, 'users/general_account_list.html', {'profiles': profiles})


from users.models import UserProfile

def account_create(request):
    if request.method == 'POST':
        # ユーザー作成
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            # UserProfile作成
            user_profile = UserProfile(user=user)
            user_profile.save()

            # その他の処理
            messages.success(request, "アカウントが作成されました。")
            return redirect('users:general_account_list')

    else:
        user_form = UserForm()
    return render(request, 'accounts/account_create.html', {'form': user_form})