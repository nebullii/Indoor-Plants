# products/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('', views.product_gallery, name='product_gallery'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('gallery/', views.product_gallery, name='product_gallery'),
    path('add/', views.add_product, name='add_product'),
    path('seller_products/', views.seller_products, name='seller_products'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('search/', views.search_plants, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
