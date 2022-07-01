from django.db import models
from rest_framework.authtoken.admin import User
from product.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
