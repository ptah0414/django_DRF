from rest_framework import serializers
from rest_framework.authtoken.admin import User

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializers
from review.serializers import ReviewSerializers


class OrderUserSerializers(serializers.ModelSerializer): # username을 보여줌
    class Meta:
        model = User
        fields = ['username', ]


class OrderProductSerializers(serializers.ModelSerializer): # name, price, seller를 보여줌
    class Meta:
        model = Product
        fields = ['name', 'price', 'seller', ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['seller'] = OrderUserSerializers(instance.seller).data # seller의 username을 보여줌

        return response


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = OrderProductSerializers(instance.product).data # product의 name, price, seller를 보여줌
        response['user'] = OrderUserSerializers(instance.user).data # user의 username을 보여줌
        return response
