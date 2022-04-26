from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import ElementViewSet

router = DefaultRouter()
router.register('', ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),

]