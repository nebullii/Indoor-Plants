from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ProductForm
from .models import Product
from cart.models import Order
from django.views import View

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_gallery(request):
    # Fetch all products from the database
    product_list = Product.objects.all().order_by('-created_at')
    
    # Set up pagination
    paginator = Paginator(product_list, 8)  # Show 6 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'products/gallery.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the seller to the currently logged-in user
            product.save()
            return redirect('product_gallery')  # Redirect to the product gallery after saving
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def seller_products(request):
    # Get all products belonging to the current logged-in vendor
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/seller_products.html', {
        'products': products
    })

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the current user is the seller of this product
    if product.seller != request.user:
        return HttpResponseForbidden("You don't have permission to edit this product.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product
    })

class BuyerDashboardView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)  # Fetch orders for the logged-in user
        return render(request, 'buyer_dashboard.html', {'orders': orders})

def home_view(request):
    # Get the 4 latest products
    latest_products = Product.objects.all().order_by('-created_at')[:4]
    return render(request, 'home.html', {'latest_products': latest_products})