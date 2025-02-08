from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.conf import settings
from django.apps import apps 
from .models import CustomUser
import re

def get_user():
    return apps.get_model(settings.AUTH_USER_MODEL)

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス','autocomplete': 'username'}),
        error_messages={
            'required': 'メールアドレスを入力してください。',
            'invalid': '有効なメールアドレスを入力してください。'
        }
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード','autocomplete': 'current-password'}),
        error_messages={'required': 'パスワードを入力してください。'}
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
        
                raise ValidationError("メールアドレスまたはパスワードが正しくありません。")
        
        return cleaned_data

def validate_hiragana(value):
    if not re.fullmatch(r'^[\u3040-\u309Fー]+$', value):
        raise ValidationError('ふりがなはひらがなのみで入力してください。')

from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
import re

class AdminSettingsForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=300,  # メールアドレスの最大長
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 255}),
        error_messages={
            'required': 'メールアドレスを入力してください。',
            'invalid': '有効なメールアドレスを入力してください。',
        },
    )

    name = forms.CharField(
    max_length=300,
    required=True,
    label="アカウント名",
    widget=forms.TextInput(attrs={'class': 'form-control','maxlength': 255}),
    error_messages={'required': 'アカウント名を入力してください。'}
)


    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name']  # nameを追加
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 300}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 300}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','maxlength': 100}),
        }

    def clean_name(self):
        """アカウント名のバリデーション"""
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("名前は必須です。")
        if len(name) > 255:
            raise ValidationError("名前は255文字以内で入力してください。")
        return name
    
    def clean_email(self):
        """メールアドレスのバリデーション"""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("メールアドレスは必須です。")
        if len(email) > 255:
            raise ValidationError("メールアドレスは255文字以下で入力してください。")
        return email

    def clean_password(self):
        """パスワードのバリデーション"""
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8 or len(password) > 32:
                raise ValidationError("パスワードは8~32文字で設定してください。")
            if not re.match(r'^[a-zA-Z0-9_-]+$', password):
                raise ValidationError("パスワードは半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            self.add_error('email', "メールアドレスは必須です。")
        if not cleaned_data.get('name'):
            self.add_error('name', "名前は必須です。")
        if not cleaned_data.get('password'):
            self.add_error('password', 'パスワードは必須です。')
        return cleaned_data


class AccountForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[('general', '一般'), ('admin', '管理者')],
        widget=forms.RadioSelect,
        label="種別", 
        required=True,
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="名前", 
        error_messages={'required':'名前を入力してください'}
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="メールアドレス", 
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )
    password = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="パスワード", 
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能",
        error_messages={'required': 'パスワードは必須です。'}
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="プロフィール画像", 
    )
    furigana = forms.CharField(
        max_length=255,
        required=False,
        validators=[validate_hiragana],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="ふりがな", 
        error_messages={'invalid': 'ふりがなはひらがなのみで入力してください。'},)
    
    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="性別", 
        required=False,
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="年齢", 
        max_value=999,
        error_messages={
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。'
        }
    )
    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="自己紹介", 
    )

    class Meta:
        model = CustomUser
        fields = ['name','email', 'password', 'furigana', 'gender', 'age', 'bio', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.model = get_user() 

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')

        if account_type == 'admin':
            if not cleaned_data.get('password'):
                self.add_error('password', '管理者アカウントの場合、パスワードは必須です。')
        return cleaned_data

class EditProfileForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '名前を入力してください'}
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'メールアドレスは必須です。'}
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = None  # ✅ 遅延評価
        fields = ['name', 'email', 'profile_image', 'bio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.model = get_user()

class UserSettingsForm(forms.ModelForm):  # ✅ `UserSettingsForm` 追加
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'メールアドレスは必須です。'}
    )

    class Meta:
        model = None  # ✅ 遅延評価
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.model = get_user()
