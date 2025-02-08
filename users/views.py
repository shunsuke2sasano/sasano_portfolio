from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import EmailUpdateForm, PasswordUpdateForm, UserProfileEditForm

def users_dashboard(request):
    return render(request, 'users/users_dashboard.html')

def users_settings(request):
    if request.method == 'POST':
        email_form = EmailUpdateForm(request.POST, instance=request.user)
        password_form = PasswordUpdateForm(request.POST)
        if email_form.is_valid() and password_form.is_valid():
            email_form.save()
            request.user.set_password(password_form.cleaned_data['password'])
            request.user.save()
            messages.success(request, '設定が更新されました。')
            return redirect('users/users_dashboard.html')
        else:
            messages.error(request, '入力内容にエラーがあります。')
    else:
        email_form = EmailUpdateForm(instance=request.user)
        password_form = PasswordUpdateForm()
    return render(request, 'users/users_settings.html', {
        'email_form': email_form,
        'password_form': password_form,
    })

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')  # ダッシュボード画面にリダイレクト
    else:
        form = UserProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})