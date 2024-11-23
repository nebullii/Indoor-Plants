from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from orders.models import Order, ShippingAddress
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe
import json

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    subtotal = cart.get_subtotal()
    shipping_cost = 5.00  # You might want to move this to settings.py
    total = cart.get_total()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': "{:.2f}".format(shipping_cost),
        'total': total,
    }
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:view_cart')

@login_required
def update_cart(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        data = json.loads(request.body) if request.body else request.POST
        quantity = int(data.get('quantity', 0))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            cart = cart_item.cart
            
            return JsonResponse({
                'success': True,
                #'message': 'Cart updated successfully',
                'item_total': "{:.2f}".format(cart_item.get_total()),
                'cart_subtotal': "{:.2f}".format(cart.get_subtotal()),
                'cart_total': "{:.2f}".format(cart.get_total()),
                'cart_count': cart.get_total_items()
            })
        else:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_subtotal': "{:.2f}".format(cart.get_subtotal()),
                'cart_total': "{:.2f}".format(cart.get_total()),
                'cart_count': cart.get_total_items()
            })
            
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid quantity specified'
        })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:view_cart')

@method_decorator(csrf_protect, name='dispatch')
class PlaceOrderView(View):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        shipping_address = ShippingAddress.objects.filter(
            user=request.user, 
            is_default=True
        ).first()
        
        if not shipping_address:
            messages.error(request, 'Please add a shipping address.')
            return redirect('orders:shipping_address_list')
        
        try:
            # Create order with shipping address
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address
            )
            
            # Create order items from cart items
            for cart_item in cart.cartitem_set.all():
                order.orderitem_set.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear the cart
            cart.cartitem_set.all().delete()
            
            messages.success(request, 'Your order has been placed successfully.')
            return redirect('orders:order_success', order_id=order.id)
            
        except Exception as e:
            messages.error(request, 'There was an error placing your order. Please try again.')
            print(f"Error placing order: {e}")
            return redirect('cart:view_cart')

class CreateCheckoutSession(View):
    def post(self, request):
        # logic to create a checkout session with Stripe
        pass  # Replace with actual implementation