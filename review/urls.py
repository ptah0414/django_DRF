from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import product.views
import review.views


urlpatterns = [
    path('review/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/<int:rid>', review.views.ReviewDetail.as_view())
]
