from unicodedata import name
from .models import Coin
from .serializers import CoinSerializer
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
                coins = Coin.objects.get(name__icontains=request.GET.get('name'))
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
