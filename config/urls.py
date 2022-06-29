from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import product.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('', include('product.urls')),
    path('', include('review.urls'))
]
