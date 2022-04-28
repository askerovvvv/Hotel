from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import ElementViewSet, Favourite
from applications.review.views import Review, DetailReview

router = DefaultRouter()
router.register('', ElementViewSet)

urlpatterns = [
    path('review/', Review.as_view()),
    path('detail/<int:pk>/', DetailReview.as_view()),
    path('favourite/', Favourite.as_view()),
    path('', include(router.urls)),

]