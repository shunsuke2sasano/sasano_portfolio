# Generated by Django 5.1.6 on 2025-02-09 14:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_managers_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='likes_received',
            field=models.ManyToManyField(related_name='received_likes', to=settings.AUTH_USER_MODEL, verbose_name='いいねを受け取ったユーザー'),
        ),
        migrations.AlterField(
            model_name='like',
            name='liked_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_likes_from_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='likes',
            field=models.ManyToManyField(related_name='profile_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
