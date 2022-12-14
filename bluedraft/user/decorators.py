from functools import wraps
from rest_framework import status
from rest_framework.response import Response
import jwt
import os


def api_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        token = request.request.COOKIES.get('jwt')
        if token is not None:
            try:
                payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            except Exception:   # jwt.ExpiredSignatureError:
                return Response({'message': "Error: Unauthenticated..."}, status=status.HTTP_401_UNAUTHORIZED)    # if the token is expired or something else, refuse
            if payload:
                return function(request, *args, **kwargs)
        return Response({'message': "Error: Unauthenticated..."}, status=status.HTTP_401_UNAUTHORIZED)
    return wrap
