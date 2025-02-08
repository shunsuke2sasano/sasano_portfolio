from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
import re

User = get_user_model()  # カスタムユーザーモデルを取得

class EmailUpdateForm(forms.Form):
    email = forms.EmailField(
        label="新しいメールアドレス",
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '新しいメールアドレスを入力してください'}),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise forms.ValidationError("メールアドレスは255文字以下である必要があります。")
        return email


class PasswordUpdateForm(forms.Form):
    password = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新しいパスワードを入力してください'}),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # パスワードのバリデーション: 8~32文字、半角英数字と _ - のみ許可
        if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise forms.ValidationError("パスワードは8〜32文字の半角英数字と「_」「-」のみ使用できます。")
        return password


class UserProfileEditForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="プロフィール画像",
        help_text="画像サイズは2MB以内でアップロードしてください。"
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="名前",
        error_messages={'required': '名前を入力してください。'}
    )
    furigana = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="ふりがな",
        error_messages={'invalid': 'ふりがなはひらがなのみで入力してください。'}
    )
    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="性別"
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        label="年齢",
        error_messages={
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。',
        }
    )
    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="自己紹介"
    )

    class Meta:
        model = User
        fields = ['name', 'profile_image', 'furigana', 'gender', 'age', 'bio']

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

    def clean_furigana(self):
        furigana = self.cleaned_data.get('furigana')
        if furigana and not re.match(r'^[ぁ-んー]+$', furigana):  # ひらがなのみ許可
            raise ValidationError("ふりがなはひらがなのみで入力してください。")
        return furigana


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User  # カスタムユーザーモデルを使用
        fields = ['name', 'email', 'bio']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User  # カスタムユーザーモデルを使用
        fields = ['email']
