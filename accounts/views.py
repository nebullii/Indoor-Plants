from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import get_user_model
from orders.models import Order
from django.db.models import Sum, F
from products.models import Product

User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")  # Fixed typo: removed space
    template_name = "registration/signup.html"

@login_required
def buyer_dashboard(request):
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_orders = orders.count()
    recent_orders = orders[:5]  # Get 5 most recent orders
    
    context = {
        'orders': recent_orders,
        'total_orders': total_orders,
    }
    return render(request, 'buyer_dashboard.html', context)

@login_required
def seller_dashboard(request):
    return render(request, 'seller_dashboard.html')

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser) 

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Get overall statistics
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(
        total=Sum(F('orderitem__price') * F('orderitem__quantity'))
    )['total'] or 0
    
    # Get recent orders with user information
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2) if total_revenue else 0,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })

@login_required
def cart_view(request):
    return render(request, 'cart.html')