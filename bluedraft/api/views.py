import jwt
import os
from .models import Coin, Wallet
from django.contrib.auth.models import User
from .serializers import CoinSerializer, WalletSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.decorators import api_login_required


class CoinAPI(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_login_required
    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('name'):
                coins = Coin.objects.filter(name=request.GET.get('name')).values()
            else:
                coins = Coin.objects.all()
            serializer = CoinSerializer(coins, many=True)
            return Response({'message': "Success", 'coins': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "Error: coin not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def post(self, request, *args, **kwargs):
        try:
            coin = Coin.objects.create(name=request.data['name'])
        except:
            return Response({'message': "Error: coin not added"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CoinSerializer(coin)
        return Response({'message': "Success", 'coin': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def put(self, request, id, *args, **kwargs):
        try:
            coin = Coin.objects.get(id=id)
        except:
            return Response({'message': "Error: coin not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        coin.name = request.data['name']
        coin.wallet = Wallet.objects.get(id=3)
        coin.save()
        serializer = CoinSerializer(coin)
        return Response({'message': "Success", 'coin': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def delete(self, request, id, *args, **kwargs):
        try:
            coin = Coin.objects.get(id=id)
        except:
            return Response({'message': "Error: coin not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        Coin.objects.filter(id=id).delete()
        serializer = CoinSerializer(coin)
        return Response({'message': "Success", 'coin': serializer.data}, status=status.HTTP_202_ACCEPTED)


class WalletAPI(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_login_required
    def get(self, request, *args, **kwargs):
        token = jwt.decode(request.COOKIES['jwt'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        #try:
        user = User.objects.get(id=token['id'])
        wallet = Wallet.objects.get(user=user)
        coins = Coin.objects.filter(wallet=wallet)
        print(coins)

        coinserilizer = CoinSerializer(coins, many=True)
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_200_OK)
        #except:
        return Response({'message': "Error: wallet not found..."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        token = jwt.decode(request.COOKIES['jwt'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        try:
            user = User.objects.get(id=token['id'])
            wallet = Wallet.objects.create(
                                            name=request.data['name'],
                                            user=user
                                            )
        except:
            return Response({'message': "Error: wallet not added..."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_200_OK)
