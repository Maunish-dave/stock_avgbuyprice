from django.db.models import Sum

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from .models import StockActions, SplitAction
from .serializers import StockaActionsSerializer,SpiltActionsSerializer

class Home(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request):
        return Response({"message":"This is a home page"}, status=status.HTTP_200_OK)


class StockActionView(ListCreateAPIView):
    
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = StockaActionsSerializer
    queryset = StockActions.objects.all()

class SplitActionView(ListCreateAPIView):
    
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = SpiltActionsSerializer
    queryset = SplitAction.objects.all()


class AvgBuyPriceView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self,request):
        total_buy = StockActions.objects.filter(trade_type='BUY').aggregate(Sum('quantity'))['quantity__sum']
        total_sell = StockActions.objects.filter(trade_type='SELL').aggregate(Sum('quantity'))['quantity__sum']
        
        total_buy = 0 if total_buy is None else total_buy
        total_sell = 0 if total_sell is None else total_sell
        
        closing_quantity = (total_buy - total_sell)
        
        current_sum = -(total_sell)
        closing_value = 0
        
        all_values = StockActions.objects.order_by('date').values_list('trade_type','quantity','price')
        
        splits = SplitAction.objects.order_by('date').values_list('ratio')
        
        for row in all_values:
            # print(row)
            if row[0] == "BUY":
                current_sum += row[1]
                if current_sum > 0:
                    closing_value += (min(current_sum,row[1])*row[2])
            elif row[0] == "SELL":
                current_sum = 0
                
        avg_buy_price = float(closing_value/closing_quantity)
        
        for split in splits:
            # print(split)
            avg_buy_price /= split[0]
            
            
        data = {"avg_buy_price":avg_buy_price}
    
        return Response(data,status=status.HTTP_200_OK)