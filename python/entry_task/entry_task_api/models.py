from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = 'categories'
    name = models.CharField(max_length=120)
    level = models.IntegerField(default=0)
    parent_category = models.ForeignKey('self', blank=True, null=True)

# Register your models here.
class Product(models.Model):
    class Meta:
        db_table = 'products'
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

class ProductCategory(models.Model):
    class Meta:
        db_table = 'product_categories'
    product = models.ForeignKey(Product)
    category = models.ForeignKey(Category)

class ProductImage(models.Model):
    class Meta:
        db_table = 'product_images'
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=120)