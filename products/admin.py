from django.contrib import admin
from .models import Product  # Import your Product model

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'seller', 'image', 'created_at', 'updated_at') 