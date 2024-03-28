
from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator
from django.conf import settings

class Cart(models.Model):
    products = models.ManyToManyField(Product, related_name='carts', through='CartProduct')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.user.username} - #{self.pk}"
    
    def calculate_total_price(self):
        total_price = 0
        cart_products = self.cartproduct_set.all()
        for cart_product in cart_products:
            total_price += cart_product.product.price * cart_product.quantity
        return total_price

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
