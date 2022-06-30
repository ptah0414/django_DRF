from rest_framework.routers import DefaultRouter
from django.urls import path, include

import order.views

router = DefaultRouter()
router.register('order', order.views.OrderViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
