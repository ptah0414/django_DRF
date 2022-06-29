from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializers


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인한 사용자만 접근 가능함

    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        qs = super().get_queryset()

        search_name = self.request.query_params.get('name',) # 쿼리의 이름 가져오기

        if search_name:
            qs = qs.filter(name__icontains=search_name) # 원하는 이름만 가져오기

        return qs

    @action(detail=False, methods=['get'], url_path="search/(?P<name>[^/.]+)")
    def search(self, request, name=None):
        qs = self.get_queryset().filter(name__icontains=name)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)