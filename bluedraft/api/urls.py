from django.urls import path
from .views import CoinAPI
from user.views import ApiLogin, APIRegister


urlpatterns = [
    # API
    path('api/coin/', CoinAPI.as_view(), name='api_coin'),
    path('api/coin/<int:id>', CoinAPI.as_view(), name='api_coin_delete'),
    path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/register/', APIRegister.as_view(), name='api_register'),
]
