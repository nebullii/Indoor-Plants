from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   ROLE_CHOICES = (
       ('BUYER', 'Buyer'),
       ('SELLER', 'Seller'),
       ('ADMIN', 'Admin'),
   )
   role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER')

   def is_buyer(self):
       return self.role == 'BUYER'

   def is_seller(self):
       return self.role == 'SELLER'

   def is_admin(self):
       return self.role == 'ADMIN'