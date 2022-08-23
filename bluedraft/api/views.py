from xml.dom import ValidationErr
import jwt
import os
import requests
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
        except ValidationErr:
            return Response({'message': "Error: coin not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def post(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=request.data['wallet'])
            coin = Coin.objects.create(name=request.data['name'], wallet=wallet)
        except (Wallet.DoesNotExist, KeyError):
            coin = Coin.objects.create(name=request.data['name'])
        except ValidationErr:
            return Response({'message': "Error: coin not added"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CoinSerializer(coin)
        return Response({'message': "Success", 'coin': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def put(self, request, id, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=request.data['wallet'])
            coin = Coin.objects.get(id=id)
            coin.wallet = wallet
        except Wallet.DoesNotExist:
            try:
                coin = Coin.objects.get(id=id)
            except Coin.DoesNotExist:
                return Response({'message': "Error: coin not found..."}, status=status.HTTP_404_NOT_FOUND)

        coin.name = request.data['name']
        coin.save()
        serializer = CoinSerializer(coin)
        return Response({'message': "Success", 'coin': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def delete(self, request, id, *args, **kwargs):
        try:
            coin = Coin.objects.get(id=id)
        except Coin.DoesNotExist:
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
        try:
            wallet = Wallet.objects.get(user__id=token['id'])
            serializer = WalletSerializer(wallet)
        except Wallet.DoesNotExist:
            return Response({'message': "Error: wallet not found..."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def post(self, request, *args, **kwargs):
        token = jwt.decode(request.COOKIES['jwt'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        if 'send' in request.path:
            return self.sendCoins(self, request.data, token['id'])
        try:
            user = User.objects.get(id=token['id'])
            wallet = Wallet.objects.create(
                                            name=request.data['name'],
                                            user=user
                                            )
        except ValidationErr:
            return Response({'message': "Error: wallet not added..."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_200_OK)

    @api_login_required
    def put(self, request, *args, **kwargs):
        token = jwt.decode(request.COOKIES['jwt'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        try:
            wallet = Wallet.objects.get(user__id=token['id'])
            wallet.name = request.data['name']
            wallet.save()
        except Wallet.DoesNotExist:
            return Response({'message': "Error: wallet not found..."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_202_ACCEPTED)

    @api_login_required
    def delete(self, request, *args, **kwargs):
        token = jwt.decode(request.COOKIES['jwt'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        try:
            wallet = Wallet.objects.get(user__id=token['id'])
        except Wallet.DoesNotExist:
            return Response({'message': "Error: wallet not added..."}, status=status.HTTP_400_BAD_REQUEST)
        Wallet.objects.filter(user__id=token['id']).delete()
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_202_ACCEPTED)

    @api_login_required
    def sendCoins(self, request, data, user_id, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(user__id=user_id)
            coins = Coin.objects.filter(wallet=wallet, name=data['coin'])
            wallet_receiver = Wallet.objects.get(user__id=data['user-receiver-id'])
            if len(coins) >= data['amount']:    # Enough founds
                count = 0
                for coin in coins:
                    if count < data['amount']:  # Send the specified amount
                        coin.wallet = wallet_receiver
                        coin.save()
                        count += 1
                    else:
                        break
            else:
                return Response({'message': "Error: insufficient funds..."}, status=status.HTTP_401_UNAUTHORIZED)
        except Wallet.DoesNotExist:
            return Response({'message': "Error: transfer not made..."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = WalletSerializer(wallet)
        return Response({'message': "Success", 'wallet': serializer.data}, status=status.HTTP_202_ACCEPTED)
