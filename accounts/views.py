from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import get_user_model

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")  # Fixed typo: removed space
    template_name = "registration/signup.html"

@login_required
def buyer_dashboard(request):
    return render(request, 'buyer_dashboard.html')

@login_required
def seller_dashboard(request):
    return render(request, 'seller_dashboard.html')

def is_admin(user):
    return user.is_authenticated and user.is_admin()   

@user_passes_test(is_admin)
def admin_dashboard(request):
    User = get_user_model()
    context = {
        'total_users': User.objects.count(),
        'total_products': 0,
        'total_orders': 0,
        'total_revenue': 0,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def cart_view(request):
    return render(request, 'cart.html')