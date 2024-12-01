from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from orders.models import Order
from products.models import Product
from django.views.generic import ListView
from django.contrib.auth.decorators import user_passes_test
from accounts.models import CustomUser 
from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Count
from django.db.models.functions import TruncMonth


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.role == 'ADMIN')

@user_passes_test(is_admin_user)
def dashboard(request):
    # Get total orders count
    total_orders = Order.objects.count()
    
    # Get total products count
    total_products = Product.objects.count()

    # Get total sellers count
    total_sellers = CustomUser.objects.filter(role='SELLER').count()

    # Fetch the latest 5 orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:3]

    # Fake data for graphs
    sales_data = [10, 25, 15, 30, 20, 35]  # Sample sales data
    revenue_growth = [1000, 1500, 1200, 1800, 1600, 2000]  # Sample revenue data
    verified_sellers = [5, 10, 15, 20, 25, 30]  # Sample verified sellers data

    # Additional fake data for new graphs
    bar_data = [12, 19, 3, 5, 2, 3]  # Sample data for bar chart
    pie_data = [300, 50, 100];  # Sample data for pie chart

    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_sellers': total_sellers,
        'sales_data': sales_data,
        'revenue_growth': revenue_growth,
        'verified_sellers': verified_sellers,
        'bar_data': bar_data,
        'pie_data': pie_data,
        'recent_orders': recent_orders,  # Pass recent orders to the context
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@user_passes_test(is_admin_user)
def order_detail(request, order_id):
    # Get the order with all related data
    order = get_object_or_404(
        Order.objects.select_related('user', 'shipping_address')
                    .prefetch_related('orderitem_set__product'),
        id=order_id
    )
    
    context = {
        'order': order,
        'items': order.orderitem_set.all(),
    }
    return render(request, 'orders/details.html', context)

@user_passes_test(is_admin_user)
def order_list(request):
    # Get the latest 5 orders with related user and order items for efficient querying
    orders = Order.objects.select_related('user').prefetch_related('orderitem_set').order_by('-created_at')[:5]
    
    # Prepare orders with their totals
    orders_with_totals = []
    for order in orders:
        orders_with_totals.append({
            'id': order.id,
            'user': order.user,
            'created_at': order.created_at,
            'total_amount': order.total,  # Using the total property from your model
            'status': order.get_status_display()  # Adding status for future use
        })
    
    context = {
        'orders': orders_with_totals,
    }
    return render(request, 'orders/list.html', context)

@user_passes_test(is_admin_user)
def sellers_list(request):
    sellers = CustomUser.objects.filter(role='SELLER')  # Fetch all sellers
    context = {
        'sellers': sellers,
    }
    return render(request, 'admin_dashboard/sellers/list.html', context)

@user_passes_test(is_admin_user)
def verify_seller(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id, role='SELLER')
    seller.is_verified = True
    seller.save()
    return redirect('admin_dashboard:sellers')  # Redirect back to sellers list

@user_passes_test(is_admin_user)
def activate_seller(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id, role='SELLER')
    seller.is_active = True
    seller.save()
    return redirect('admin_dashboard:sellers')

@user_passes_test(is_admin_user)
def deactivate_seller(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id, role='SELLER')
    seller.is_active = False
    seller.save()
    return redirect('admin_dashboard:sellers')

@user_passes_test(is_admin_user)
def seller_statistics(request):
    total_sellers = CustomUser.objects.filter(role='SELLER').count()
    verified_sellers = CustomUser.objects.filter(role='SELLER', is_verified=True).count()
    inactive_sellers = CustomUser.objects.filter(role='SELLER', is_active=False).count()

    context = {
        'total_sellers': total_sellers,
        'verified_sellers': verified_sellers,
        'inactive_sellers': inactive_sellers,
    }
    return render(request, 'admin_dashboard/sellers/statistics.html', context)

@user_passes_test(is_admin_user)
def all_products(request):
    products = Product.objects.all()  # Fetch all products
    context = {
        'products': products,
    }
    return render(request, 'products/list.html', context)  # Adjust the template path as needed

