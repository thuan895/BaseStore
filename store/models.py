from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.db.models.fields import BooleanField, CharField, DateTimeField, FloatField, IntegerField, SlugField, TextField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.

class Product(models.Model):
    product_name    = CharField(max_length=500, unique=True)
    slug            = SlugField(max_length=500, unique=True)
    description     = TextField(max_length=1000, blank=True)
    price           = IntegerField()
    images          = ImageField(upload_to='photos/products')
    stock           = IntegerField()
    is_available    = BooleanField(default=True)
    category        = ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = DateTimeField(auto_now_add=True)
    modified_date   = DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self):
        return self.product_name
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg =0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size','size'),
)
class Variation(models.Model):
    product             = ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = CharField(max_length=100, choices=variation_category_choice)
    variation_value     = CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = DateTimeField(auto_now=True)
    
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product     = ForeignKey(Product, on_delete=models.CASCADE)
    user        = ForeignKey(Account, on_delete=models.CASCADE)
    subject     = CharField(max_length=500, blank=True)
    review      = TextField(max_length=1000, blank=True)
    rating      = FloatField()
    ip          = CharField(max_length=20, blank=True)
    status      = BooleanField(default=True)
    created_at= DateTimeField(auto_now_add=True)
    updated_at= DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
