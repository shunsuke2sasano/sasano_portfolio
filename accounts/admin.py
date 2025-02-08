from django.contrib import admin
try:
    from .models import UserProfile
except ImportError:
    UserProfile = None

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'updated_at', 'deleted_at')  # 新しいフィールドを追加
    search_fields = ('user__username', 'name') 

# Register your models here.
