from django.urls import path
import review.views

urlpatterns = [
    path('review/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/', review.views.ReviewList.as_view()),
    path('review/<int:pid>/<int:rid>/', review.views.ReviewDetail.as_view())
]
