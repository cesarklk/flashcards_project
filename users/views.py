from django.shortcuts import render
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer
import logging
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Datos de registro recibidos: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Usuario registrado exitosamente: {serializer.data.get('email', 'No email provided')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.error(f"Errores de validación en registro: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"Login exitoso para el usuario: {user.email}")
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        logger.error(f"Errores de validación en login: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def home(request):
    return Response({"message": "Bienvenido a la API de Flashcards"})

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Request: {request.method} {request.path}")
        logger.debug(f"Headers: {request.headers}")
        response = self.get_response(request)
        logger.debug(f"Response status: {response.status_code}")
        return response