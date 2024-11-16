from django.contrib import admin
from .models import Cart, CartItem, Order

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Number of empty forms to display

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'get_total']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'added_at', 'get_total']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'cart')