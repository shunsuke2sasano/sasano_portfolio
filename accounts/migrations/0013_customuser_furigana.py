# Generated by Django 5.1.6 on 2025-02-14 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20250214_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='furigana',
            field=models.CharField(default='ふりがな', max_length=255, verbose_name='ふりがな'),
        ),
    ]
