from django import forms
from .models import Inquiry, Category

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body', 'status']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=300,
        label="名前",  # ここでラベルを「名前」に変更
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 300}),
        error_messages={'max_length': '名前は255文字以内で入力してください。'}
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 255:
            raise forms.ValidationError("名前は255文字以内で入力してください。")
        return name

    class Meta:
        model = Category
        fields = ['name']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body', 'status']  # ステータスは管理画面で使用

class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body']  # ステータスを除外

class InquiryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['status']  # ステータスのみ変更可能
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'ステータス',
        }