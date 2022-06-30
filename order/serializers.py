from rest_framework import serializers
from rest_framework.authtoken.admin import User

from order.models import Order
from product.models import Product


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'seller', ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['seller'] = \
            OrderUserSerializer(instance.seller).data

        return response


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = \
            OrderProductSerializer(instance.product).data
        response['user'] = \
            OrderUserSerializer(instance.user).data
        return response
