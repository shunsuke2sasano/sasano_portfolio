# Generated by Django 5.1.6 on 2025-02-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_customuser_furigana'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='自己紹介'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=300, unique=True, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='furigana',
            field=models.CharField(max_length=300, verbose_name='ふりがな'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=300, unique=True, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='generaluserprofile',
            name='furigana',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='ふりがな'),
        ),
        migrations.AlterField(
            model_name='generaluserprofile',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='generaluserprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='プロフィール画像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='furigana',
            field=models.CharField(default='ふりがな', max_length=300, verbose_name='ふりがな'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')], max_length=20, verbose_name='性別'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=300, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='プロフィール画像'),
        ),
    ]
