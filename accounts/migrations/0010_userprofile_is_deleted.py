# Generated by Django 5.1.6 on 2025-02-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='削除フラグ'),
        ),
    ]
