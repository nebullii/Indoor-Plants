from django.db import models
from django.contrib.auth import get_user_model

class Product(models.Model):
    
    name = models.CharField(max_length=255)  # Name of the plant
    description = models.TextField()          # Description of the plant
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the plant
    image = models.ImageField(upload_to='products/')  # Image of the plant
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Seller of the plant
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the product was last updated
    featured = models.BooleanField(default=False)  # Whether the product is featured
    hot_selling = models.BooleanField(default=False)  # Whether the product is hot selling

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name