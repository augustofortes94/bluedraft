from .models import Coin, Wallet
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'name', 'date_created', 'date_updated']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'coins', 'user']
