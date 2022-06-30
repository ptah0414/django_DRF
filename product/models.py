from django.db import models
from rest_framework.authtoken.admin import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    discount_percentage = models.IntegerField()
    is_free_delivery = models.BooleanField()
    is_on_sale = models.BooleanField()

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/product/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)