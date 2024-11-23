import stripe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cart.models import Cart
from orders.models import ShippingAddress, Order
from django.conf import settings
import json

stripe.api_key = settings.STRIPE_SECRET_KEY  

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    shipping_address = ShippingAddress.objects.filter(user=request.user, is_default=True).first()

    if not shipping_address:
        messages.warning(request, 'Please add a shipping address first.')
        return redirect('orders:shipping_address_select')

    context = {
        'cart': cart,
        'shipping_address': shipping_address,
        'shipping_cost': settings.SHIPPING_COST,
        'total': cart.get_total(),
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/checkout.html', context)

@login_required
def process_payment(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_total = float(cart.get_total())
            shipping_cost = float(settings.SHIPPING_COST)
            total_amount = cart_total + shipping_cost
            total_amount_cents = int(total_amount * 100)  # Convert to cents

            # Create PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=total_amount_cents,
                currency='usd',
                metadata={
                    'user_id': str(request.user.id),
                    'cart_id': str(cart.id),
                },
                automatic_payment_methods={'enabled': True}
            )

            # Store payment_intent_id in session
            request.session['payment_intent_id'] = intent.id
            request.session.modified = True

            return JsonResponse({
                'clientSecret': intent.client_secret,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def payment_success(request):
    payment_intent_id = request.session.get('payment_intent_id')
    
    try:
        # Verify the payment intent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == 'succeeded':
            cart = Cart.objects.get(user=request.user)
            shipping_address = ShippingAddress.objects.get(user=request.user, is_default=True)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                status='PROCESSING',
                shipping_cost=settings.SHIPPING_COST
            )
            
            # Create order items from cart items
            cart_items = list(cart.cartitem_set.all())
            for cart_item in cart_items:
                order.orderitem_set.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear cart after successful order creation
            cart.cartitem_set.all().delete()
            
            # Clear session
            del request.session['payment_intent_id']
            
            messages.success(request, 'Payment successful! Thank you for your order.')
            return render(request, 'payments/success.html', {'order': order})
        
        messages.error(request, 'Payment verification failed.')
        return render(request, 'payments/success.html')
        
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'payments/success.html')
    
    
@login_required
def payment_cancel(request):
    return render(request, 'payments/cancel.html')