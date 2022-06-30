from dj_rest_auth.app_settings import serializers
from django.db.models import Avg
from django.http import JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer


def detail(request, pid):
    product = Product.objects.get(id=pid)
    total = 0
    for review in product.review_set.all():
        total += review.score

    product_detail = {
        'id': product.id,
        'name': product.name,
        'original_price': int(product.price),
        'discount_percentage': int(product.discount_percentage),
        'discount_price': int(product.price) * (100 - int(product.discount_percentage)) // 100,
        'company': product.seller.username,
        'image': ['http://127.0.0.1:8000/media/'+productimage.image.name for productimage in product.productimage_set.all()],
        'rate_average': round(total/ product.review_set.count()),
        'review_count': product.review_set.count(),
        'delivery_type': '배송',
        'delivery_period': 3,
        'delivery_fee': 0,
        'is_free_delivery': True,
        'is_on_sale': not (int(product.discount_percentage) == 0),
        'size': list(set(['대', '중', '소'])),
        'color': list(set(['빨', '주', '노'])),
    }
    return JsonResponse({'product': product_detail}, status=200)


def review(request, pid):
    product = Product.objects.get(id=pid)

    results = [{
        "review_id": product_review.id,
        "review_content": product_review.contents,
        "review_image": 'test',
        "review_rate": product_review.score,
        "product_name": product_review.product.name,
        "day": str('2022-06-30').split(" ")[0],
        "review_user_name": product_review.writer.username,
        "review_like": True,
    } for product_review in product.review_set.all()]

    return JsonResponse({'results': results}, status=200)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return obj.owner == request.user


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def create(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(seller=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        search_name = self.request.query_params.get('name', )

        if search_name:
            qs = qs.filter(name__icontains=search_name)

        return qs

    @action(detail=False, methods=['get'], url_path="search/(?P<name>[^/.]+)")
    def search(self, request, name=None):
        qs = self.get_queryset().filter(name__icontains=name)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)
