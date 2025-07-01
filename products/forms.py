# products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'featured', 'hot_selling', 'in_stock', 'category', 'tags', 'status']
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Add CSS classes and ensure id and name attributes are set
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-name',
            'name': 'product_name'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-description',
            'name': 'product_description'
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'id': 'product-price',
            'name': 'product_price'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file',
            'id': 'product-image',
            'name': 'product_image'
        })
        self.fields['featured'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'product-featured',
            'name': 'product_featured'
        })
        self.fields['hot_selling'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'product-hot-selling',
            'name': 'product_hot_selling'
        })

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for plants', max_length=100)