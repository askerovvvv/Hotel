from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, LoginSerializer, CustomSerializer

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Отправлен активационный код'
            return Response(message, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)       # else


class ActivateView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code) #@@@@@@@@@@@@@@@@@@@@@@@@@@@
            user.is_active = True
            user.activation_code = '' #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            user.save()
            return Response("Ваш аккаунт активен!")
        except User.DoesNotExist:
            return Response('Активационный код не действителен!')


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class CustomView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(email=user)
        return queryset