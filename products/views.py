from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_gallery(request):
    # Sample product data, replace with actual data if needed
    products = [
    {
        "name": "Monstera deliciosa",
        "description": "A tropical plant with large, glossy, split leaves known for its air-purifying qualities.",
        "price": "$25"
    },
    {
        "name": "Spider Plant",
        "description": "A hardy houseplant with arching green leaves, famous for producing 'babies' that can be easily propagated.",
        "price": "$15"
    },
    {
        "name": "White Bird of Paradise",
        "description": "A majestic plant with large banana-like leaves that produces unique, bird-like flowers when mature.",
        "price": "$20"
    },
    # Add more plants as needed
    ]
    
    return render(request, 'products/gallery.html', {'products': products})
