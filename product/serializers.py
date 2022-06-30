from rest_framework import serializers

from product.models import Product
from review.serializers import ReviewSerializers

class ProductSerializers(serializers.ModelSerializer):
    review_set = ReviewSerializers(many=True, read_only=True) # 리뷰는 등록 안해도 되게 read_only
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'review_set', 'review_count']
