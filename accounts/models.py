from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now
from django.db import models

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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("スーパーユーザーは is_staff=True にする必要があります。")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("スーパーユーザーは is_superuser=True にする必要があります。")

        return self.create_user(name, email, password, **extra_fields)

# カスタムユーザーモデル
class CustomUser(AbstractUser, TimestampedModel):  
    username = None  
    name = models.CharField(max_length=255, unique=True) 
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False) 
    bio = models.TextField(max_length=1500, blank=True, null=True)  
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/default.jpg')
    is_deleted = models.BooleanField(default=False)  

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["name"] 

    objects = CustomUserManager() 

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        """論理削除を実現するためのオーバーライドメソッド"""
        super(CustomUser, self).delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """論理削除されたデータの復元"""
        self.is_deleted = False
        self.save()

    class Meta:
        ordering = ['-created_at']  # デフォルトの並び順

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

    likes = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    
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
    liked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes_received")
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
