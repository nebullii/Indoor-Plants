from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem, Order
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total = cart.get_total()
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{quantity} x {product.name} added to cart.')
        return redirect('view_cart')
    
    return redirect('product_gallery')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@method_decorator(csrf_protect, name='dispatch')
class PlaceOrderView(View):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        try:
            order = Order.objects.create(user=request.user, cart=cart)
            cart.cartitem_set.all().delete()
            messages.success(request, 'Your order has been placed successfully.')
        except Exception as e:
            messages.error(request, 'There was an error placing your order. Please try again.')
            print(f"Error placing order: {e}")

        return redirect('home')
    
class CreateCheckoutSession(View):
    def post(self, request):
        # Your logic to create a checkout session with Stripe
        pass  # Replace with actual implementation