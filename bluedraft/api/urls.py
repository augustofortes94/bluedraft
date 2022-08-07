from django.urls import path
from user.views import ApiLogin, APIRegister


urlpatterns = [
    # API
    path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/register/', APIRegister.as_view(), name='api_register'),
]
