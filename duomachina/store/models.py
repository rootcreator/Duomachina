from django.db import models
from users.models import User
from media.models import Media
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    MEDIA_TYPE = 'media'
    MERCH_TYPE = 'merch'
    PRODUCT_TYPES = [
        (MEDIA_TYPE, 'Media'),
        (MERCH_TYPE, 'Merch'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(choices=PRODUCT_TYPES, max_length=5)
    artist = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def is_media(self):
        return self.product_type == self.MEDIA_TYPE

    @property
    def is_merch(self):
        return self.product_type == self.MERCH_TYPE

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

class Commission(models.Model):
    artist = models.ForeignKey(User, related_name='commissions', on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name='commissions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission for {self.artist.username} from Order #{self.order_item.order.id}"
