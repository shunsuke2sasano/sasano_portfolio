# Generated by Django 5.1.6 on 2025-02-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(max_length=20, null=True, verbose_name='性別'),
        ),
    ]
