from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import order.views

router = DefaultRouter()
router.register('order', order.views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]

