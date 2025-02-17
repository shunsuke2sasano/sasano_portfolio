from django.db import models
from django import forms


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  


class Category(TimestampedModel):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False) 

    def physical_delete(self, using=None, keep_parents=False):
        super(Category, self).delete(using=using, keep_parents=keep_parents)
        """物理削除"""

        
    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', '未対応'),
        ('in_progress', '対応中'),
        ('resolved', '対応済み'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    body = models.TextField()  # お問い合わせ内容を格納するフィールド
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.category.name}: {self.body[:20]}..."  # contentをbodyに修正

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


