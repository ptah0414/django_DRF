from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import product.views
import review.views


router = DefaultRouter()
router.register('product', product.views.ProductViewSet)
# router.register('review', review.views.ReviewAPI)

urlpatterns = [
    path('', include(router.urls))
]

