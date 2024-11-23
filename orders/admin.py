from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'total']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_address__full_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

    def total(self, obj):
        return f"${obj.total:.2f}"
    total.short_description = 'Total Amount'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__status']
    search_fields = ['order__user__username', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'is_default']
    list_filter = ['is_default', 'state', 'city']
    search_fields = ['full_name', 'user__username', 'address']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')