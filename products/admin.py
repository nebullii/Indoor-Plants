from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'seller', 'featured', 'hot_selling', 'created_at']
    list_filter = ['featured', 'hot_selling', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['featured', 'hot_selling', 'price']