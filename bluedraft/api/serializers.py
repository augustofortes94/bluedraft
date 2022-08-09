from .models import Coin
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['name', 'date_created', 'date_updated']