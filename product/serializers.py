from rest_framework import serializers
from rest_framework.authtoken.admin import User
from product.models import Product, ProductImage
from review.serializers import ReviewSerializer


class ProductUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image',]



class ProductSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=False)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    productimage_set = ProductImageSerializer(many=True, read_only=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'review_count', 'productimage_set', 'review_set', 'discount_percentage', 'is_free_delivery', 'is_on_sale',]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = instance.seller.username
        response['image'] = response['productimage_set'][0]['image']
        response['discount_price'] = instance.price * (100 - instance.discount_percentage) // 100
        if response['review_count'] != 0:
            total = 0
            for review in instance.review_set.all():
                total += review.score
            response['rate_average'] = \
                round(total / response['review_count'], 1)
        else:
            response['rate_average'] = 0

        return response
