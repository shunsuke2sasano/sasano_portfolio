from django.urls import path
from . import views
from .views import inquiry_create

app_name = 'inquiry'

urlpatterns = [
    path('', views.inquiry_list, name='inquiry_list'),
    path('<int:id>/', views.inquiry_detail, name='inquiry_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('create/', inquiry_create, name='inquiry_create'),
]
