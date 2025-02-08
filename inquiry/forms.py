from django import forms
from .models import Inquiry, Category

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body', 'status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body', 'status']  # ステータスは管理画面で使用

class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body']  # ステータスを除外