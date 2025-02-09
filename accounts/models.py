from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError


# ✅ `common` を削除し、直接 `TimestampedModel` を定義
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# カスタムユーザーマネージャー
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # 🔥 is_staff を True にする
        extra_fields.setdefault("is_superuser", True)  # 🔥 is_superuser を True にする

        if extra_fields.get("is_staff") is not True:
            raise ValueError("スーパーユーザーは is_staff=True にする必要があります。")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("スーパーユーザーは is_superuser=True にする必要があります。")

        return self.create_user(name=name, email=email, password=password, **extra_fields)
    
# カスタムユーザーモデル
class CustomUser(AbstractUser, PermissionsMixin):
    username = None  # ユーザーネームは使用しない
    name = models.CharField(max_length=255, unique=True, verbose_name="名前")
    email = models.EmailField(max_length=255, unique=True, verbose_name="メールアドレス")
    is_admin = models.BooleanField(default=False, verbose_name="管理者フラグ")
    is_staff = models.BooleanField(default=False, verbose_name="スタッフフラグ")  # 🔥 追加
    bio = models.TextField(
        max_length=1500,
        blank=True,
        null=True,
        verbose_name="自己紹介"
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/default_profile_image.jpg',
        verbose_name="プロフィール画像"
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="年齢"
    )
    STATUS_CHOICES = [
        ('active', '有効'),
        ('inactive', '無効'),
    ]
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="ステータス"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")

    objects = CustomUserManager()  # 🔥 Manager を設定

    likes_received = models.ManyToManyField(
    "self",
    symmetrical=False,
    related_name="received_likes_custom",
    verbose_name="いいねを受け取ったユーザー"
    )

    USERNAME_FIELD = "email"  # 認証に使用するフィールド
    REQUIRED_FIELDS = ["name"]

    def clean(self):
        """年齢のバリデーション"""
        if self.age is not None and (self.age < 0 or self.age > 999):
            raise ValidationError({'age': '年齢は0以上999以下で入力してください。'})

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        """論理削除: データを物理削除せずフラグで管理"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """論理削除されたデータの復元"""
        self.is_deleted = False
        self.save()

    class Meta:
        ordering = ['-id']
        verbose_name = "カスタムユーザー"
        verbose_name_plural = "カスタムユーザー一覧"

# 一般ユーザーのプロフィールモデル
class UserProfile(models.Model):
    """一般ユーザーのプロフィールモデル"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  # ✅ ユーザーが削除されたら、このレコードも削除
        related_name='user_profile'
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    likes = likes = models.ManyToManyField(
    CustomUser,
    related_name="profile_likes"  # ✅ `liked_profiles` と被らないよう変更
)
    
    def delete(self, using=None, keep_parents=False):
        """論理削除を行うメソッド"""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """論理削除されたデータを復元"""
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        """削除済みかどうかを判定"""
        return self.deleted_at is not None
    
    def __str__(self):
        return self.user.email if self.user else "未設定ユーザー"

# いいね機能のモデル
class Like(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes_given")
    liked_user = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    related_name="likes_received_records",  # 修正
)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name="profile_likes", null=True, blank=True)
    def __str__(self):
        return f"{self.user} likes {self.liked_user}"

    class Meta:
        unique_together = ('user', 'liked_user','profile')
    
# 一般ユーザーの詳細プロフィールモデル
class GeneralUserProfile(models.Model):
    """ 一般ユーザーの詳細プロフィールモデル """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE  # ✅ ユーザーが削除されたら、このレコードも削除
    )
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')],
        blank=True, 
        null=True
    )  
    likes_count = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.user.email if self.user else "未設定ユーザー"
