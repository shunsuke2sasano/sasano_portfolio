from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.conf import settings
from django.apps import apps 
from .models import CustomUser, UserProfile
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


def validate_hiragana(value):
    """ひらがなバリデーション（ひらがな・長音のみ許可）"""
    if value and not re.match(r'^[\u3040-\u309Fー]+$', value):  # ひらがな・長音（ー）のみ
        raise ValidationError('ふりがなはひらがなのみで入力してください。')

class AccountForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[('general', '一般'), ('admin', '管理者')],
        widget=forms.RadioSelect,
        label="種別",
        required=True,
    )
    STATUS_CHOICES = [
        ('active', '有効'),
        ('inactive', '無効'),
    ]

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="名前",
        error_messages={'required': '名前を入力してください。'}
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
        label="プロフィール画像"
    )

    furigana = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="ふりがな",
        validators=[validate_hiragana],
        error_messages={'invalid': 'ふりがなはひらがなのみで入力してください。'},
    )

    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="年齢",
        min_value=0,
        max_value=999,
        error_messages={
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。',
        }
    )

    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="自己紹介",
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="ステータス",
        initial='active',
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'profile_image', 'furigana', 'age', 'bio', 'status']

    def clean_password(self):
        """パスワードバリデーション"""
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean_profile_image(self):
        """プロフィール画像バリデーション"""
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')

        if account_type == 'general':
            if not cleaned_data.get('furigana'):
                self.add_error('furigana', 'ふりがなを入力してください。')
            if not cleaned_data.get('age'):
                self.add_error('age', '年齢を入力してください。')

        return cleaned_data

User = get_user_model()

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
        model = CustomUser  # ✅ 修正
        fields = ['name', 'email', 'profile_image', 'bio']

class UserSettingsForm(forms.ModelForm):  # ✅ `UserSettingsForm` 追加
    email = forms.EmailField(
        max_length=300,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'maxlength':'300'}),
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )

    new_password = forms.CharField(
        max_length=50,
        required=False,  # パスワード変更しない場合もあるため
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'maxlength':'50'}),
        label="新しいパスワード",
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能",
    )

    def clean_email(self):
        """メールアドレスのバリデーション"""
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise ValidationError("メールアドレスは255文字以内で入力してください。")
        return email

    def clean_new_password(self):
        """パスワードのバリデーション"""
        password = self.cleaned_data.get('new_password')
        if password:
            if len(password) < 8 or len(password) > 32:
                raise ValidationError("パスワードは8~32文字で設定してください。")
            if not re.match(r'^[a-zA-Z0-9_-]+$', password):
                raise ValidationError("パスワードは半角英数字と'_'、'-'のみ使用可能です。")
        return password
    
    class Meta:
        model = CustomUser
        fields = ['email']

class AccountEditForm(forms.ModelForm):
    is_active = forms.ChoiceField(
        choices=[(True, "有効"), (False, "無効")],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="ステータス",
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'profile_image', 'bio', 'is_active']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return self.instance.password  # 変更なし
        if len(password) < 8 or len(password) > 32:
            raise ValidationError("パスワードは8~32文字で設定してください。")
        return password

class AccountEditForm(forms.ModelForm):
    """管理者用アカウント編集フォーム"""
    
    name = forms.CharField(
        max_length=255,
        required=True,
        label="アカウント名",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'アカウント名を入力してください。'}
    )

    furigana = forms.CharField(
        max_length=255,
        required=True,
        label="ふりがな",
        validators=[validate_hiragana],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'ふりがなを入力してください。'}
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。'
        }
    )

    password = forms.CharField(
        max_length=32,
        required=False,
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能"
    )

    profile_image = forms.ImageField(
        required=False,
        label="プロフィール画像",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性')],
        required=True,
        label="性別",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': '性別を選択してください。'}
    )

    age = forms.IntegerField(
        required=True,
        label="年齢",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        min_value=0,
        max_value=999,
        error_messages={
            'required': '年齢を入力してください。',
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。'
        }
    )

    bio = forms.CharField(
        max_length=1500,
        required=False,
        label="自己紹介",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        help_text="1500文字以内で入力してください。"
    )

    is_active = forms.ChoiceField(
        choices=[('True', "有効"), ('False', "無効")],
        required=True,
        label="ステータス",
        widget=forms.RadioSelect,
        error_messages={'required': 'ステータスを選択してください。'}
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'furigana', 'email', 'password', 'profile_image', 'gender', 'age', 'bio', 'is_active']

    # バリデーション
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise ValidationError("メールアドレスは255文字以下で入力してください。")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and (len(password) < 8 or len(password) > 32 or not re.match(r'^[a-zA-Z0-9_-]+$', password)):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=256,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )

    new_password = forms.CharField(
        max_length=32,
        required=False,  # パスワード変更しない場合もあるため
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="新しいパスワード",
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能",
    )

    def clean_email(self):
        """メールアドレスのバリデーション"""
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise ValidationError("メールアドレスは255文字以内で入力してください。")
        return email

    def clean_new_password(self):
        """パスワードのバリデーション"""
        password = self.cleaned_data.get('new_password')
        if password:
            if len(password) < 8 or len(password) > 32:
                raise ValidationError("パスワードは8~32文字で設定してください。")
            if not re.match(r'^[a-zA-Z0-9_-]+$', password):
                raise ValidationError("パスワードは半角英数字と'_'、'-'のみ使用可能です。")
        return password

    class Meta:
        model = CustomUser
        fields = ['email', 'new_password']

class EditProfileForm(forms.ModelForm):
    def clean_profile_image(self):
        """プロフィール画像のバリデーション (2MB制限)"""
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB (バイト換算)
            raise ValidationError("画像サイズは2MB以下にしてください。")
        return image

    def clean_name(self):
        """名前のバリデーション (255文字制限)"""
        name = self.cleaned_data.get('name')
        if len(name) > 255:
            raise ValidationError("名前は255文字以内で入力してください。")
        return name

    def clean_furigana(self):
        """ふりがなのバリデーション (255文字制限 & ひらがなのみ)"""
        furigana = self.cleaned_data.get('furigana')
        if len(furigana) > 255:
            raise ValidationError("ふりがなは255文字以内で入力してください。")
        if not re.match(r'^[ぁ-んー]+$', furigana):  # ひらがなのみ許可
            raise ValidationError("ふりがなはひらがなのみ入力してください。")
        return furigana

    def clean_gender(self):
        """性別のバリデーション (男性・女性のみ)"""
        gender = self.cleaned_data.get('gender')
        if gender not in ['male', 'female']:
            raise ValidationError("性別は「男性」または「女性」を選択してください。")
        return gender

    def clean_age(self):
        """年齢のバリデーション (0-999のみ許可)"""
        age = self.cleaned_data.get('age')
        if age is not None:
            if not (0 <= age <= 999):
                raise ValidationError("年齢は0〜999の範囲で入力してください。")
        return age

    def clean_bio(self):
        """自己紹介のバリデーション (1500文字制限)"""
        bio = self.cleaned_data.get('bio')
        if len(bio) > 1500:
            raise ValidationError("自己紹介は1500文字以内で入力してください。")
        return bio

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'name', 'furigana', 'gender', 'age', 'bio']