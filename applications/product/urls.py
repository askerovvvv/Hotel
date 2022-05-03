from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import ElementViewSet, Favourite, ReservationView, create_hotel_view, \
    ReservationHistory
from applications.review.views import Review, DetailReview

router = DefaultRouter()
router.register('', ElementViewSet)

urlpatterns = [
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('review/', Review.as_view()),
    path('reserv/', ReservationView.as_view()),
    path('reserv-history/', ReservationHistory.as_view()),
    path('detail/<int:pk>/', DetailReview.as_view()),
    path('favourite/', Favourite.as_view()),
    path('parser/', create_hotel_view),
    path('', include(router.urls)),
    # path('favourite-history/', ),
]