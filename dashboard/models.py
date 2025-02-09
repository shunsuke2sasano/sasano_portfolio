from django.db import models
from django.utils.timezone import now
from django.conf import settings

class DashboardSettings(models.Model):
    """管理者向けのダッシュボード設定（例）"""
    site_maintenance = models.BooleanField(default=False)
    announcement = models.TextField(blank=True)

    def __str__(self):
        return "Dashboard Settings"

