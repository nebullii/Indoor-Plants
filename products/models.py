from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    CATEGORY_TYPES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='indoor')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ]
    
    name = models.CharField(max_length=255)  # Name of the plant
    description = models.TextField()          # Description of the plant
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the plant
    image = models.ImageField(upload_to='products/')  # Image of the plant
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Seller of the plant
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the product was last updated
    featured = models.BooleanField(default=False)  # Whether the product is featured
    hot_selling = models.BooleanField(default=False)  # Whether the product is hot selling
    in_stock = models.BooleanField(default=True)  # Whether the product is in stock
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    about = models.TextField(blank=True, null=True)
    care_tip = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name