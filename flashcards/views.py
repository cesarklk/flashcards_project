from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Flashcard
from .serializers import FlashcardSerializer

import logging

logger = logging.getLogger(__name__)

class FlashcardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"User: {self.request.user}, Auth: {self.request.auth}")
        return Flashcard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        logger.debug(f"Creando flashcard para el usuario: {self.request.user}")
        serializer.save(user=self.request.user)

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        print(f"Datos de login recibidos: {data}")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                response = {'success': True}
                print(f"Respuesta enviada: {response}")
                return JsonResponse(response)
            else:
                response = {'success': False, 'error': 'Credenciales inválidas'}
                print(f"Respuesta enviada: {response}")
                return JsonResponse(response, status=400)
        except User.DoesNotExist:
            response = {'success': False, 'error': 'Usuario no encontrado'}
            print(f"Respuesta enviada: {response}")
            return JsonResponse(response, status=400)
    return JsonResponse({'error': 'Método de solicitud inválido'}, status=405)

import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Request: {request.method} {request.path}")
        logger.debug(f"Headers: {request.headers}")
        response = self.get_response(request)
        logger.debug(f"Response status: {response.status_code}")
        return response