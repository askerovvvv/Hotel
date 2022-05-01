from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.product.models import *
from applications.product.sendmessage import sendTelegram
from applications.product.serializers import *
from applications.review.models import Like, Rating
from applications.review.serializers import RatingSerializer
from parser import main


class LargeResultsSetPagination(PageNumberPagination):
    """
    Представление пагинации
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ElementViewSet(ModelViewSet):
    """
    Представление отелей
    """
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(methods=['POST'], detail=True)
    def carp(self, request, pk):
        element_id = Element.objects.get(id=pk)
        category_of_element = element_id.category
        recomendation_element = Element.objects.filter(category=category_of_element)
        serializer = ElementSerializer(recomendation_element, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        element = self.get_object()
        like_obj, _ = Like.objects.get_or_create(element=element, user=request.user)
        print(like_obj)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(element=self.get_object(), user=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(user=request.user, element=self.get_object(), rating=request.data['rating'])

        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Favourite(ListCreateAPIView):
    """
    Представление избранных
    """
    queryset = FavouriteElement.objects.all()
    serializer_class = FavouriteElementSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        # print('\n\n', self.request.data, '\n\n')
        serializer.save(user=self.request.user)


# TODO fawf


class ReservationView(CreateAPIView):
    """
    Представление бронировании отелей
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer, ):
        serializer.save(user=self.request.user)


class ReservationHistory(ListAPIView):
    """
    Представление истории бронировании отелей
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer,):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset


@api_view(['GET'])
def create_hotel_view(request):
    """
    Представление парсинга
    """
    hotels = main()
    for i in hotels:
        title = i.get('title')
        rating = i.get('rating')
        ratingcount = i.get('ratingcount')
        image = i.get('image')

        HotelsIk.objects.create(title=title, ratingcount=ratingcount, rating=rating, image=image)
    return Response(hotels)




    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
