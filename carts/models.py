from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from store.models import Product, Variation
from accounts.models import *
# Create your models here.

class Cart(models.Model):
    cart_id     = CharField(max_length=250, blank=True)
    date_added  = DateField(auto_now_add=True)
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user        = ForeignKey(Account, on_delete=models.CASCADE, null = True)
    product     = ForeignKey(Product, on_delete=models.CASCADE)
    variations  = ManyToManyField(Variation, blank=True)
    cart        = ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity    = IntegerField()
    is_active   = BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name