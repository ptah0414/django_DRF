from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
