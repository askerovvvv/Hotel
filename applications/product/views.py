from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.product.models import *
from applications.product.serializers import *
from applications.review.models import Like, Rating
from applications.review.serializers import RatingSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ElementViewSet(ModelViewSet):
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
    queryset = FavouriteElement.objects.all()
    serializer_class = FavouriteElementSerializer

    # def post(self, request, *args, **kwargs):
    #     obj = request.data
    #     print(obj)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        # print('\n\n', self.request.data, '\n\n')
        serializer.save(user=self.request.user)


    # def music_detail(request, id):
    #     try:
    #         music = Music.objects.get(id=id)
    #         serializer = MusicSerializer(music, many=False)
    #         return Response(serializer.data)
    #     except Music.DoesNotExist:
    #         raise Http404
    #



    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
