from .models import Coin, Wallet
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'name', 'date_created', 'date_updated', 'wallet']


class CoinShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'name', 'date_updated']


class WalletSerializer(serializers.ModelSerializer):
    coins = CoinShortSerializer(read_only=True, many=True)    

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'user', 'coins']
