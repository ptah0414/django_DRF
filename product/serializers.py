from rest_framework import serializers

from product.models import Product


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', ]
    #
    # def save(self): # save 메소드 오버라이드하기
    #     name = self.validated_data['name']
    #     description = self.validated_data['description']
    #     price = self.validated_data['price']
    #     seller = self.context['request'].user # 로그인한 user를 받아옴
