from django.db import models
from django.db.models.fields import CharField, SlugField, TextField
from django.db.models.fields.files import ImageField
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name   = CharField(max_length=500, unique=True)
    slug            = SlugField(max_length=500, unique=True)
    description     = TextField(max_length=500, blank=True)
    cat_image       = ImageField(upload_to='photos/categories', blank=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    def __str__(self):
        return self.category_name
        