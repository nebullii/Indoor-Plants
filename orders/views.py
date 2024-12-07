from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShippingAddress, Order
from .forms import ShippingAddressForm
from decimal import Decimal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def shipping_address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'orders/shipping_address_list.html', {'addresses': addresses})

@login_required
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Shipping address added successfully!')
            return redirect('orders:shipping_address_list')
    else:
        form = ShippingAddressForm()
    return render(request, 'orders/shipping_address_form.html', {'form': form})

@login_required
def edit_shipping_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipping address updated successfully!')
            return redirect('orders:shipping_address_list')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'orders/shipping_address_form.html', 
                 {'form': form, 'editing': True})

@login_required
def set_default_address(request, pk):
    if request.method == 'POST':
        address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
        # Remove default from other addresses
        ShippingAddress.objects.filter(user=request.user).update(is_default=False)
        # Set new default
        address.is_default = True
        address.save()
        messages.success(request, 'Default shipping address updated.')
    return redirect('orders:shipping_address_list')

@login_required
def order_review(request):
    if request.method != 'POST':
        return redirect('orders:shipping_address_select')
    
    cart = request.user.cart
    cart_items = cart.cartitem_set.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:view_cart')
    
    address_id = request.POST.get('address_id')
    shipping_address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    
    subtotal = sum(item.get_total for item in cart_items)
    shipping_cost = Decimal('5.00')
    total = subtotal + shipping_cost
    
    context = {
        'cart_items': cart_items,
        'shipping_address': shipping_address,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'orders/order_review.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        cart = request.user.cart
        shipping_address = ShippingAddress.objects.filter(
            user=request.user, 
            is_default=True
        ).first()
        
        if not shipping_address:
            messages.error(request, 'Please add a shipping address.')
            return redirect('orders:shipping_address_list')
        
        try:
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address
            )
            
            for cart_item in cart.cartitem_set.all():
                order.orderitem_set.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            cart.cartitem_set.all().delete()
            messages.success(request, 'Order placed successfully!')

            return redirect('orders:order_success', order_id=order.id)
            
        except Exception as e:
            messages.error(request, 'There was an error placing your order.')
            return redirect('cart:view_cart')
    
    return redirect('orders:order_review')


@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def shipping_address_select(request):
    # Check if cart is empty
    if not request.user.cart.cartitem_set.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:view_cart')
    
    # Get user's addresses
    addresses = ShippingAddress.objects.filter(user=request.user)
    
    # If no addresses exist, redirect to add address page
    if not addresses.exists():
        messages.info(request, 'Please add a shipping address to continue.')
        return redirect('orders:add_shipping_address')
    
    context = {
        'addresses': addresses,
        'default_address': addresses.filter(is_default=True).first()
    }
    return render(request, 'orders/select_address.html', context)

@login_required
def proceed_to_payment(request, address_id):
    if request.method != 'POST':
        return redirect('orders:shipping_address_select')
    
    try:
        # Get and set the selected address as default
        shipping_address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
        
        # Set all addresses to non-default first
        ShippingAddress.objects.filter(user=request.user).update(is_default=False)
        
        # Set selected address as default
        shipping_address.is_default = True
        shipping_address.save()
        
        # Redirect to payment checkout
        return redirect('payments:checkout')
    
    except ShippingAddress.DoesNotExist:
        messages.error(request, 'Invalid shipping address selected.')
        return redirect('orders:shipping_address_select')
    
@login_required
def order_detail(request, order_id):
    # For regular users, show only their own orders
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'orders/order_detail.html', {'order': order})