from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator

from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('visa', 'Pay by Visa'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders',through='OrderProduct')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

class PaymentHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField()


    def __str__(self):
        return self.product.name
    