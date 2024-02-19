from decimal import Decimal
from django.conf import settings
from django.db import models
from products.models import Product



class Basket(models.Model):
    """
    A model representing a basket for storing products and quantities.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.qty}"

    # Add other methods as needed

    class Meta:
        verbose_name_plural = "Baskets"