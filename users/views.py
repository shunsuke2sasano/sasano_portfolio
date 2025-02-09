from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import EmailUpdateForm, PasswordUpdateForm, UserProfileEditForm
from django.contrib.auth import get_user_model

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
