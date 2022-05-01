from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from applications.product.models import Element
from applications.review.models import Comment
from applications.review.serializers import ReviewSerializer, RetriveReviewSerializer


class Review(CreateAPIView):
    """
    Представление отзывов
    """
    queryset = Comment.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailReview(RetrieveAPIView):
    """
    Представление для детального отзыва с отзывами
    """
    serializer_class = RetriveReviewSerializer
    queryset = Element.objects.all()


