from django.urls import path
from .views import CoinAPI, WalletAPI
from user.views import ApiLogin, APIRegister


urlpatterns = [
    # API
    path('api/coin/', CoinAPI.as_view(), name='api_coin'),
    path('api/coin/<int:id>', CoinAPI.as_view(), name='api_by_id'),
    path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/register/', APIRegister.as_view(), name='api_register'),
    path('api/wallet/', WalletAPI.as_view(), name='api_wallet'),
    path('api/wallet/<int:id>', WalletAPI.as_view(), name='api_wallet_by_id'),
]
