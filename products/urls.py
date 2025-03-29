# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_gallery, name='product_gallery'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('seller/', views.seller_products, name='seller_products'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
]