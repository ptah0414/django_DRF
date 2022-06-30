from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.admin import User

from product.models import Product


class Review(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)]
    )
    contents = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

