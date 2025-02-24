# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, GeneralUserProfile

@receiver(post_save, sender=CustomUser)
def sync_general_user_profile(sender, instance, created, **kwargs):
    """
    CustomUser が保存されたときに GeneralUserProfile を自動作成・更新する。
    - 作成時: ユーザーが一般アカウントなら GeneralUserProfile を作成する。
    - 更新時: GeneralUserProfile が存在すれば、CustomUser の情報を同期する。
    """
    if created:
        # 一般ユーザーなら GeneralUserProfile を作成
        if not instance.is_staff and not instance.is_superuser:  # 一般ユーザーのみ
            GeneralUserProfile.objects.create(
                user=instance,
                name=instance.name,
                furigana=instance.furigana,
                bio=instance.bio,
                age=instance.age,
                gender=instance.gender,
                profile_image=instance.profile_image,
                likes_count=0,
            )
    else:
        # 既存の GeneralUserProfile を更新
        if not instance.is_staff and not instance.is_superuser:  # 一般ユーザーのみ
            try:
                profile = instance.generaluserprofile  # OneToOneField の reverse 関連
            except GeneralUserProfile.DoesNotExist:
                profile = GeneralUserProfile.objects.create(
                    user=instance,
                    name=instance.name,
                    furigana=instance.furigana,
                    bio=instance.bio,
                    age=instance.age,
                    gender=instance.gender,
                    profile_image=instance.profile_image,
                    likes_count=0,
                )
            else:
                profile.name = instance.name
                profile.furigana = instance.furigana
                profile.bio = instance.bio
                profile.age = instance.age
                profile.gender = instance.gender
                profile.profile_image = instance.profile_image
                profile.save()
