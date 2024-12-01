from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from orders.models import Order
from django.views import View

def home(request):
    featured_products = Product.objects.filter(featured=True).order_by('-created_at')[:4]
    hot_selling_products = Product.objects.filter(hot_selling=True).order_by('-created_at')[:4]
    context = {
        'featured_products': featured_products,
        'hot_selling_products': hot_selling_products,
    }
    return render(request, 'home.html', context)

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
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products:product_gallery')  # Add namespace
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
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:seller_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/add_product.html', {
        'form': form,
        'product': product
    })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    return redirect('products:seller_products')  # Redirect back to the seller products page

class BuyerDashboardView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)  # Fetch orders for the logged-in user
        return render(request, 'buyer_dashboard.html', {'orders': orders})