from django.db import transaction
from .models import Order

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, shipping_address, cart):
        """Create a new order from cart"""
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address
        )
        
        # Create order items from cart items
        for cart_item in cart.cartitem_set.all():
            order.orderitem_set.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        return order

    @staticmethod
    def get_order_details(order):
        """Get order details for display"""
        return {
            'items': order.orderitem_set.all(),
            'subtotal': order.subtotal,
            'shipping_cost': order.shipping_cost,
            'total': order.total,
            'shipping_address': order.shipping_address,
            'status': order.status
        }