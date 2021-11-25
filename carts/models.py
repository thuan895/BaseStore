from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField
from django.db.models.fields.related import ForeignKey
from store.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id     = CharField(max_length=250, blank=True)
    date_added  = DateField(auto_now_add=True)
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product     = ForeignKey(Product, on_delete=models.CASCADE)
    cart        = ForeignKey(Cart, on_delete=models.CASCADE)
    quantity    = IntegerField()
    is_active   = BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name