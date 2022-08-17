import datetime
import jwt
import os
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiLogin(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        user = User.objects.filter(username=request.data['username']).first()
        if user is None:
            return Response({'message': "Error: user not found..."}, status=status.HTTP_404_NOT_FOUND)

        else:
            if not user.check_password(request.data['password']):
                return Response({'message': "incorrect password..."}, status=status.HTTP_401_UNAUTHORIZED)

            payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                    }
            token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {'message': "Succes"}
            return response


class APIRegister(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Succes'}, status=status.HTTP_200_OK)
