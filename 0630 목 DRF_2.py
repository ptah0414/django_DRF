product/views.py 수정 

def perform_create(self, serializer):
    serializer.save(seller=self.request.user)
    
    
prefetch related와 같은 기능하는 것 만들기

주문 만들기: 상품-사용자-주문 사이의 관계 
사용자 1           N 주문 만들기 M          1 상품
=> 사용자와 상품 사이의 다대 다 관계 


flab 출신 프로젝트 봐보기 
wecode 부트캠프 프로젝트 봐보기
https://github.com/wecode-bootcamp-korea/17-1st-SweetHome-frontend
오늘의 집 클론코딩 코드 zip 받기 

nodejs 14버전 설치하기 
chocolatey 체크해서 설치하기 - 쿠버네티스에서도 쓰일 수 있음

cd C:\Users\user\Downloads\17-1st-SweetHome-frontend-master\17-1st-SweetHome-frontend-master
npm install
npm start 

src/config.js
장고의 drf 서버로 바꾸기 -> 127.0.0.1:8000
export const SERVER = "http://127.0.0.1:8000";
export const CARTSERVER = "http://127.0.0.1:8000";

=================================================================================================

상품과 리뷰 사이의 관계 맺어주기 
review/models.py 
product = models.ForeignKey(Product, on_delete=models.CASCADE)

1:N 관계일 때
1측을 기준으로 N측을 같이 조회 -> 리뷰
N측을 기준으로 1측을 같이 조회 -> 주문 

product/serializers.py
class ProductSerializers(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=True) # 리뷰는 등록 안해도 되게 read_only
    
review/serializers.py
class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['score', 'contents', ]
        
review/urls.py
url에 pid와 rid 수정 
urlpatterns = [
    path('review/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/<int:rid>', review.views.ReviewDetail.as_view())
]

review/views.py
post 함수에서 pid 추가
ReviewDetail에서 pid, rid 추가 
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


product/serializers.py
review_count 추가
class ProductSerializers(serializers.ModelSerializer):
    review_set = ReviewSerializers(many=True, read_only=True) # 리뷰는 등록 안해도 되게 read_only
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'review_set', 'review_count']
        
=================================================================================================

startapp order 

order/models.py 
from rest_framework.authtoken.admin import User

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

order/views.py
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    
order/serializers.py 생성
class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
order/urls.py 생성
router = DefaultRouter()
router.register('order', order.views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]


config/urls.py
path('', include('order.urls')) 추가 

INSTALLED_APP 에 'order' 추가 

makemigrations, migrate 

order/admin.py 생성 
admin.site.register(Order)


사용자 1        N 주문 만들기 M        1 상품

order/serializers.py 
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



==================================================================

주문 조회 만들기  
    로그인 되어있어야 함
    자기 자신의 주문 정보만 조회할 수 있어야 함
    메소드 재정의하기 
    
order/views.py 

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def get_query(self):
        qs = super().get_queryset()
                
        qs = qs.filter(user=self.request.user)
        return qs


product/models.py 추가 
class Product(models.Model):
    ...
    discount_percentage = models.IntegerField()
    is_free_delivery = models.BooleanField()
    is_on_sale = models.BooleanField()


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/product/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

product/admin.py
admin.site.register(ProductImage) 추가

product/serializers.py 수정
class ProductSerializers(serializers.ModelSerializer):
    ...
    fields = ['id', 'name', 'review_count', 'review_set', 'discount_percentage', 'is_free_delivery', 'is_on_sale']

media 추가    
settings.py
MEDIA_URL = '/media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

urls.py 경로 추가 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


pip install pillow 
makemigrations, migrate 


product/serializers.py 
ProductSerializers에 to_representation 함수 작성 

def to_representation(self, instance):
    response = super().to_representation(instance)
    response['company'] = instance.seller.username
    response['discount_price'] = instance.price * (100 - instance.discount_percentage) // 100

    if instance.review_count != 0:
        total = 0
        for review in instance.review_set.all():
            total += review.score
        response['rate_average'] = round(total // response['review_count'], 1) # 소수 한 자리만 나오게 반올림
    else:
        response['rate_average'] = 0


Image Serializers 만들기 
product/serializers.py 
class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']
        
class ProductSerializers(serializers.ModelSerializer):
    ...
    productimage_set = ProductImageSerializers(many=True, read_only=False)
    ...
    def to_representation(self, instance):
        ...
        response['image'] = response['productimage_set'][0]['image']


127.0.0.1:8000/product 접속하면 CORS 오류 발생 
이유?
프론트엔드는 127.0.0.1:8000(리액트)이고 백엔드는 localhost:3000(장고)으로 도메인이 다르기 때문에 

pip install django-cors-headers 

INSTALLED_APP = ['corsheaders']

MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']

CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000', 'http://localhost:3000']

CORS_ALLOW_CREDENTIALS = True


http://localhost:3000/productmain 접속해보기 -> 이미지랑 상품 목록 잘 조회됨


=========================================================================
product detail 만들기

product/urls.py
urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pid>', product.views.detail),
    path('products/<int:pid>/review', product.views.review),
]


product/views.py
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


=========================================================================
API 명세서 만들기 - swagger 자동으로 API Documentations 명세서를 만들어줌

