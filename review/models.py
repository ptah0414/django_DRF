from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.admin import User
from django.db import models

class Review(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator (5)])
    contents = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)