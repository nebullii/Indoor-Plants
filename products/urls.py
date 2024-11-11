# products/urls.py
from django.urls import path
from .views import product_detail, product_gallery, add_product

urlpatterns = [
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('gallery/', product_gallery, name='product_gallery'),
    path('add/', add_product, name='add_product'),
]