from django.shortcuts import render, get_object_or_404, redirect
from .models import Inquiry, Category
from .forms import InquiryForm, CategoryForm, InquiryCreateForm, InquiryStatusUpdateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# お問い合わせ一覧
@user_passes_test(is_admin)
def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'inquiry/inquiry_list.html', {'inquiries': inquiries})

# お問い合わせ詳細
@user_passes_test(is_admin)
def inquiry_detail(request, id):
    inquiry = get_object_or_404(Inquiry, id=id)

    if request.method == 'POST':
        form = InquiryStatusUpdateForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "ステータスが更新されました。")
            return redirect('inquiry:inquiry_detail', id=id)  # 更新後に同じページへリダイレクト
    else:
        form = InquiryStatusUpdateForm(instance=inquiry)

    return render(request, 'inquiry/inquiry_detail.html', {'inquiry': inquiry, 'form': form})

# カテゴリ一覧
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.filter(is_deleted=False)
    return render(request, 'inquiry/category_list.html', {'categories': categories})

# カテゴリ追加
@user_passes_test(is_admin)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "カテゴリーが追加されました。")
            return redirect('inquiry:category_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = CategoryForm()
    return render(request, 'inquiry/category_add.html', {'form': form})

# カテゴリ編集
@user_passes_test(is_admin)
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "カテゴリーが更新されました。")
            return redirect('inquiry:category_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inquiry/category_edit.html', {'form': form})

# カテゴリ削除
@user_passes_test(is_admin)
def category_delete(request, id):
    category = get_object_or_404(Category, id=id, is_deleted=False)
    if request.method == 'POST':
        # 「未登録」カテゴリを取得または作成（未登録カテゴリがなければ作成）
        default_category, created = Category.objects.get_or_create(
            name='未登録',
            defaults={'is_deleted': False}
        )
        # 対象カテゴリに属するお問い合わせを、未登録カテゴリに更新
        Inquiry.objects.filter(category=category).update(category=default_category)
        # カテゴリ自体を物理削除
        category.delete()
        messages.success(request, "カテゴリーが削除され、お問い合わせは「未登録」に更新されました。")
        return redirect('inquiry:category_list')
    
    return render(request, 'inquiry/category_delete.html', {'category': category})

#お問合せ作成
def inquiry_create(request):
    if request.method == "POST":
        form = InquiryCreateForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.status = 'pending'  
            inquiry.save()

            # メール送信
            send_mail(
                subject=f"新しいお問い合わせ: {inquiry.category.name}",
                message=f"カテゴリ: {inquiry.category.name}\n本文: {inquiry.body}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )

            messages.success(request, "お問い合わせが送信されました。")
            return redirect('inquiry:inquiry_list')  # 投稿後のリダイレクト先
    else:
        form = InquiryCreateForm()

    return render(request, 'inquiry/inquiry_create.html', {'form': form})