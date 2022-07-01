0629 화 - DRF 

DRF - Django Rest Framework
Rest API 서버로 만들 것임


좋아요 기능이 rest api -> 사용자에게 json 형태의 응답을 받음
return JsonResponse

new project -> web_drf
pip install django
django-admin startproject config .

pip install 3개
djangorestframework
markdown
django-filter

settings.py
INSTALLED_APP = [rest_framework’]

urls.py
path(‘api-auth/’, include(‘rest_framework.urls’))

python manage.py runserver
127.0.0.1:8000/api-auth/login/ 접속 -> …/login 으로 접속하면 not found고, …/login/으로 접속해야 함

Quickstart 참고하기
python manage.py startapp product

settings.py
INSTALLED_APP = [‘product’]


models.py
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


product/serializers.py 생성 
from rest_framework import serializers
from product.models import Product

class ProductSerializers(serializers.ModelSerializer):
    class Meta: # Meta 데이터: 데이터에 대한 데이터 (생성 날짜 등)
        model = Product
        fields = '__all__'


views.py
from rest_framework import viewsets
from product.models import Product
from product.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import product.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('product.urls'))
]


product/urls.py 생성
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import product.views

router = DefaultRouter()
router.register('product', product.views.ProductViewSet)
urlpatterns = [
    path('', include(router.urls))
]


makemigrations 
migrate 
127.0.0.1:8000/product/ 접속

admin.py
from django.contrib import admin
from product.models import Product

admin.site.register(Product)

createsuperuser 
admin 로그인 후 상품 여러개 추가해보기 
/product/1
/product/2 접속해보기 

patch 수정
delete 삭제 

실제 개발에서는 advanced rest client, postman 사용함 
advanced rest client 설치하기 

http://127.0.0.1:8000/product/ -> send하면 상품이 조회됨 

http://127.0.0.1:8000/product/1/ -> delete method로 send하면 삭제됨

http://127.0.0.1:8000/product/ -> 목록을 다시 조회해보면 1번 항목이 삭제되어있음 

메소드    URL             설명       데이터
GET     product/        목록         X
POST    product/        생성 -> id를 입력하지 않는 이유? 몇 번 id가 생성될지 모르기 떄문 -> Body, application/json -> json 형식으로 작성하기 -> JSON visual editor로 선택 후, 키와 값 입력하기 
GET     product/[id]/   조회         X 
PATCH   product/[id]/   수정         Product 모델 
DELETE  product/[id]/   삭제         X

GET     product/        검색목록      Product 모델.name


views.py 
get_queryset() 오버라이딩하기
이름으로 검색하는 기능 추가해보기 
127.0.0.1:8000/product/?name=cat 으로 검색되게 만들기 

    def get_queryset(self):
        qs = super().get_queryset()

        search_name = self.request.query_params.get('name',) # 쿼리의 이름 가져오기

        if search_name:
            qs = qs.filter(name__contains=search_name) # 원하는 이름만 가져오기

        return qs
        

        
search 함수 만들기
127.0.0.1:8000/product/search/cat 으로 검색되게 만들기 

    @action(detail=False, methods=['get'], url_path="search/(?P<name>[^/.]+")
    def search(self, request, name=None):
        qs = self.get_queryset().filter(name__icontains=name)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)
        
===============================================================

startapp review

INSTALLED_APP = [’rewiew’]

review/models.py

from django.core.valitators import MinValueValidator, MaxValueValidator 
class Review(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator (5)]) 
    contents = model.TextField()

makemigrations
migrate

뒤에는 방식 동일

댓글 기능에서는 Read를 위한 페이지가 필요 없음

APIView는 원하는 기능만 사용할 수 있음

review/views.py 수정 
ModelViewSet → APIView

class ReviewList(APIView):
    def get(self, request):
        qs = Review.objects.all()
        serializer = ReviewSerializers(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializers(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get(self, request, pk):
        qs = Review.objects.get(id=pk)
        serializer = ReviewSerializers(qs, many=False)
        return Response(serializer.data)

    def patch(self, request, pk):
        qs = Review.objects.get(id=pk)
        serializer = ReviewSerializers(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = Review.objects.get(id=pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
        
review/urls.py 수정

urlpatterns = [
    path('review/', review.views.ReviewAPI.as_view()),
    path('review/<int:pk>/', review.views.ReviewDetail.as_view())
]

회원가입 기능 추가하기
startapp acounts
login, logout 기능은 이미 있으므로 APIView로 회원 가입하는 기능만 만들기
accounts/views.py
class UserAPI(APIView):
    pass
    
account/serializers.py 생성
    
pip install dj-rest-auth 설치 
pip isntall django-allauth

restAPI 같은 경우에는 일반적으로 세션 로그인이 아닌 토큰 로그인 방식을 씀
settings.py
INSTALLED_APP = [
    'django.contrib.sites'
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'product',
    'review'
]
SITE_ID = 1
INSTALLED_APP 순서 지켜야 에러가 안 남 

일반적으로 제일 많이 쓰는 토큰은 JWT(Json Web Token)

설정 바뀌었으니까 makemigrations, migrate 

urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('', include('product.urls')),
    path('', include('review.urls'))
]

https://dj-rest-auth.readthedocs.io/en/latest/installation.html#json-web-token-jwt-support-optional 참고 
pip install djangorestframework-simplejwt

settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}

REST_USE_JWT = True

JWT_AUTH_COOKIE = 'my-app-auth' # 쿠키 만료 시간을 짧게 설정함 
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' # 사용자가 이용하는데 불편함이 없게, 만료 시간을 길게 설정함 

ACCOUNT_EMAIL_VERIFICATION = "none"

 
http://127.0.0.1:8000/dj-rest-auth/registration/ 로 접속해보기 


migrate
ARC로 post 방식으로 회원가입 해보기 -> 가입 성공

http://127.0.0.1:8000/dj-rest-auth/login/ -> 로그인 성공

product/views.py 
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    

로그인 ptah0414  
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU2NDg2MzcwLCJpYXQiOjE2NTY0ODYwNzAsImp0aSI6IjU3MjEwZDk0YTE4NDQ3NTc5ZDY5YzM4OTk1MTE3ZTNlIiwidXNlcl9pZCI6MX0.7r_Q301DSeIHuKjdj8tqXhxmd0EOAVVqLs4pNpeiHjQ",
"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NjU3MjQ3MCwiaWF0IjoxNjU2NDg2MDcwLCJqdGkiOiJkZDU4NzdjYTZkNDU0ZWFkYmZjZWIzNGJjYTFhZDliMiIsInVzZXJfaWQiOjF9.X9RXHBLs5k8kJgIW2frz9I-SHTNLNXOYQYAMHTbpgDk",

GET http://127.0.0.1:8000/product/
Authorization: Bearer [access_token]
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU2NDg1OTExLCJpYXQiOjE2NTY0ODU2MTEsImp0aSI6IjI4N2VjYzQzZDM3MDQxNGI5ZDRlMTEzYmQ1MjExMGI0IiwidXNlcl9pZCI6MX0.zYE3YIBCoD8Q5biQAEvLjbQgDjuUzWWQQiUwXAACJP8

Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU2NDg1OTExLCJpYXQiOjE2NTY0ODU2MTEsImp0aSI6IjI4N2VjYzQzZDM3MDQxNGI5ZDRlMTEzYmQ1MjExMGI0IiwidXNlcl9pZCI6MX0.zYE3YIBCoD8Q5biQAEvLjbQgDjuUzWWQQiUwXAACJP8

토큰 만료 시간이 굉장히 빠르므로 안 된다면 다시 로그인해서 토큰 복붙해오기 


jwt.io 접속 -> 토큰 만료 시간 알아보기
acress_token 붙여 넣으면 exp 알 수 있음 -> "exp": 1656486370
epochconverter.com에서 시간 변환하기 
GMT: 2022년 June 29일 Wednesday AM 7:06:10
Your time zone: 2022년 6월 29일 수요일 오후 4:06:10

만료가 되었다면 refresh하기
http://127.0.0.1:8000/dj-rest-auth/token/refresh/에 POST 방식으로 refresh 토큰 보내기
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NjU3MjQ3MCwiaWF0IjoxNjU2NDg2MDcwLCJqdGkiOiJkZDU4NzdjYTZkNDU0ZWFkYmZjZWIzNGJjYTFhZDliMiIsInVzZXJfaWQiOjF9.X9RXHBLs5k8kJgIW2frz9I-SHTNLNXOYQYAMHTbpgDk"
}
새로 갱신된 access_token과 refresh_token이 출력됨 



===================================================================
상품에 판매자 추가하고 관계 맺어주기 

product/model.py
from rest_framework.authtoken.admin import User

seller = models.ForeignKey(User, on_delete=models.CASCADE)

모델 바뀌었으니 migrate 

토큰 만료로 로그인이 계속 풀리기 떄문에     
permission_classes = [IsAuthenticatedOrReadOnly] 로 설정
주석처리하기 

product/serializers.py  

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', ] # seller를 exclude하고 싶지만, exclude 필드 만드는게 안 돼서 입력 받으려고 하는 fields만 정의하기

product/views.py에 create 함수 정의하기 
class ProductViewSet(viewsets.ModelViewSet):
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
===================================================================================================================
        
리뷰에 사용자 관계 맺어주기

review/model.py
writer = models.ForeignKey(User, on_delete=models.CASCADE)

모델 바뀌었으니 migrate 


review/serializers.py  

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['score', 'contents', ] # seller를 exclude하고 싶지만, exclude 필드 만드는게 안 돼서 입력 받으려고 하는 fields만 정의하기


review/views.py에 create 함수 정의하기 
class ReviewViewSet(viewsets.ModelViewSet):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



