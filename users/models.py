from django.conf import settings
from django.db import models
from django.apps import apps

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(TimestampedModel):
    """ プロフィール詳細モデル """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_detail'
    )
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='accounts.Like',
        through_fields=('profile', 'liked_user'), related_name='liked_profiles'
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'users'


    

