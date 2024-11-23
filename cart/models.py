from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_items(self):
        """Get the total number of items in cart"""
        return sum(item.quantity for item in self.cartitem_set.all())

    def get_subtotal(self):
        """Calculate cart subtotal before shipping"""
        cart_items = self.cartitem_set.all()
        return sum(item.get_total() for item in cart_items)

    def get_shipping_cost(self):
        """Get shipping cost from settings"""
        return Decimal(str(getattr(settings, 'SHIPPING_COST', '5.00')))

    def get_total(self):
        """Calculate cart total including shipping"""
        return self.get_subtotal() + self.get_shipping_cost()

    def clear(self):
        """Remove all items from cart"""
        self.cartitem_set.all().delete()

    def update_quantity(self, product_id, quantity):
        """Update quantity for a specific product"""
        try:
            cart_item = self.cartitem_set.get(product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    def add_item(self, product, quantity=1):
        """Add item to cart or update quantity if exists"""
        cart_item, created = self.cartitem_set.get_or_create(
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def remove_item(self, product_id):
        """Remove item from cart"""
        return self.cartitem_set.filter(product_id=product_id).delete()

    def __str__(self):
        return f"Cart for {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        """Calculate total price for this item"""
        return Decimal(str(self.product.price)) * self.quantity

    def increase_quantity(self, amount=1):
        """Increase item quantity"""
        self.quantity += amount
        self.save()

    def decrease_quantity(self, amount=1):
        """Decrease item quantity"""
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        ordering = ['-added_at']
        unique_together = ['cart', 'product']  # Prevent duplicate products in cart


# Signal to create cart automatically when user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

# Signal to save cart when user is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_cart(sender, instance, **kwargs):
    try:
        instance.cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=instance)