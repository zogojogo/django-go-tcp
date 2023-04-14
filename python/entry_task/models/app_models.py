from django.db import models

class ModelManager(models.Manager):
    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class Category(models.Model):
    class Meta:
        db_table = 'categories'
    name = models.CharField(max_length=120)
    level = models.IntegerField(default=0)
    parent_category = models.ForeignKey('self', blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()

class Product(models.Model):
    class Meta:
        db_table = 'products'
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()


class ProductCategory(models.Model):
    class Meta:
        db_table = 'product_categories'
    product = models.ForeignKey(Product)
    category = models.ForeignKey(Category)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()

class ProductImage(models.Model):
    class Meta:
        db_table = 'product_images'
    product = models.ForeignKey(Product, related_name='images')
    image_url = models.CharField(max_length=120)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()

class User(models.Model):
    class Meta:
        db_table = 'users'
    username = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=1000)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()

class ProductComment(models.Model):
    class Meta:
        db_table = 'product_comments'
    product = models.ForeignKey(Product, related_name='product')
    user = models.ForeignKey(User, related_name='user')
    parent_comment = models.ForeignKey('self', blank=True, null=True)
    comment_text = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ModelManager()
