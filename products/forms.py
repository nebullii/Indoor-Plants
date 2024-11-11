# products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Add CSS classes and ensure id and name attributes are set
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-name',  # Custom id
            'name': 'product_name'  # Custom name
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-description',  # Custom id
            'name': 'product_description'  # Custom name
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-price',  # Custom id
            'name': 'product_price'  # Custom name
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file',
            'id': 'product-image',  # Custom id
            'name': 'product_image'  # Custom name
        })
