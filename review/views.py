from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Product
from review.models import Review
from review.serializers import ReviewSerializers

class ReviewList(APIView):
    def get(self, request):
        qs = Review.objects.all()
        serializer = ReviewSerializers(qs, many=True)
        return Response(serializer.data)

    def post(self, request, pid):
        serializer = ReviewSerializers(data=request.data, many=False)

        if serializer.is_valid():
            product = Product()
            product.id = pid
            serializer.save(writer=request.user, product=product)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    def get(self, request, pid, rid):
        qs = Review.objects.get(id=rid)
        serializer = ReviewSerializers(qs, many=False)
        return Response(serializer.data)

    def patch(self, request, pid, rid):
        qs = Review.objects.get(id=rid)
        serializer = ReviewSerializers(qs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = Review.objects.get(id=pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
