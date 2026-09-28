from django.db import models
from apps.accounts.models import User
from apps.artworks.models import Artwork

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    class Meta: unique_together = ('cart','artwork')

class Order(models.Model):
    STATUS = [('pending','در انتظار پرداخت'),('paid','پرداخت شده'),('shipped','ارسال شده'),('delivered','تحویل شده'),('cancelled','لغو شده')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=0)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=0) # قیمت لحظه خرید
