from rest_framework import serializers

from product.models import Product
from review.models import Review

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['score', 'contents', ]