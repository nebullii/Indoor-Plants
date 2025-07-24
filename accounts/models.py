# Keep only the CustomUser model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

class CustomUser(AbstractUser):
   ROLE_CHOICES = (
       ('BUYER', 'Buyer'),
       ('SELLER', 'Seller'),
       ('ADMIN', 'Admin'),
   )
   role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER')
   is_verified = models.BooleanField(default=False)
   business_name = models.CharField(max_length=255, blank=True, null=True)
   phone = models.CharField(max_length=20, blank=True, null=True)
   address = models.TextField(blank=True, null=True)

   def is_buyer(self):
       return self.role == 'BUYER'

   def is_seller(self):
       return self.role == 'SELLER'

   def is_admin(self):
       return self.role == 'ADMIN'