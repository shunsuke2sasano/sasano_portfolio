# Generated by Django 4.2.7 on 2025-02-09 06:32

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-id'], 'verbose_name': 'カスタムユーザー', 'verbose_name_plural': 'カスタムユーザー一覧'},
        ),
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='年齢'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=1500, null=True, verbose_name='自己紹介'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='管理者フラグ'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='削除フラグ'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default_profile_image.jpg', null=True, upload_to='profile_images/', verbose_name='プロフィール画像'),
        ),
    ]
