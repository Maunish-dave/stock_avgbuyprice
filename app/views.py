from django.db.models import Sum, F
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import StockActions, SplitAction, Holding
from .serializers import StockaActionsSerializer,SpiltActionsSerializer,HoldingSerializer, UserSerializer

class Home(APIView):
    """ Just a testing API"""
    permission_classes = (AllowAny,)
    
    def get(self,request):
        return Response({"message":"This is a home page"}, status=status.HTTP_200_OK)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class StockActionView(ListCreateAPIView):
    
    """ API for Buying and Selling a stock"""
    
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = StockaActionsSerializer
    queryset = StockActions.objects.all()
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return StockActions.objects.filter(user__id=user_id)
    
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        data = JSONParser().parse(request)
            
        serializer = StockaActionsSerializer(data=data)
        if serializer.is_valid():
            
            trade_type = serializer.validated_data['trade_type']
            quantity = serializer.validated_data['quantity']
            price = serializer.validated_data['price']
            serializer.save(user=user)

            if trade_type == "SELL":
                quantity = (-quantity)
            
            amount_invested = (price * quantity)
            
            avg_buy_price = get_avg_buy_price(user_id)
            
            #update the holdings table 
            hodling = Holding.objects.filter(user__id=user_id)
            if hodling.first() is not None:
                hodling.update(
                            quantity=F('quantity')+quantity,
                            amount_invested=F('amount_invested')+amount_invested,
                            avg_buy_price=avg_buy_price)
            else:
                holding = Holding.objects.create(user=user,
                                                quantity=quantity,
                                                amount_invested=amount_invested,
                                                avg_buy_price=avg_buy_price)
                holding.save()
                                
            return Response("success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     
     
def get_avg_buy_price(user_id):
    
    """ This functions calculates average buy price for a given the user_id"""
    
    total_buy = StockActions.objects.filter(user__id=user_id).filter(trade_type='BUY').aggregate(Sum('quantity'))['quantity__sum']
    total_sell = StockActions.objects.filter(user__id=user_id).filter(trade_type='SELL').aggregate(Sum('quantity'))['quantity__sum']
    
    total_buy = 0 if total_buy is None else total_buy
    total_sell = 0 if total_sell is None else total_sell
    
    closing_quantity = (total_buy - total_sell)
    
    current_sum = -(total_sell)
    closing_value = 0
    
    all_values = StockActions.objects.filter(user__id=user_id).order_by('date').values_list('trade_type','quantity','price')
    
    splits = SplitAction.objects.filter(user__id=user_id).order_by('date').values_list('ratio')
    
    for row in all_values:
        if row[0] == "BUY":
            current_sum += row[1]
            if current_sum > 0:
                closing_value += (min(current_sum,row[1])*row[2])
        elif row[0] == "SELL":
            current_sum = 0
            
    avg_buy_price = float(closing_value/closing_quantity)
    
    for split in splits:
        avg_buy_price /= split[0]
            
    return avg_buy_price   

class SplitActionView(ListCreateAPIView):
    
    """API for adding spilt action ratio and updating the holdings table"""
    
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = SpiltActionsSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return SplitAction.objects.filter(user__id=user_id)
    
    def post(self, request,user_id):
        user = User.objects.get(id=user_id)
        data = JSONParser().parse(request)
        serializer = SpiltActionsSerializer(data=data)
        if serializer.is_valid():
            ratio = serializer.validated_data['ratio']
            serializer.save(user=user)
            
            avg_buy_price = get_avg_buy_price(user_id)
            
            #updatet holdings 
            holding = Holding.objects.filter(user__id=user_id).update(user=user,
                                                quantity=F('quantity')*ratio,
                                                avg_buy_price=avg_buy_price)
            
            return Response("sucess", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvgBuyPriceView(APIView):
    """ API for reading average buy price for a given user_id"""
    
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self,request, user_id):
        holding = Holding.objects.filter(user__id=user_id).first()
        serializer = HoldingSerializer(holding, many=False)
        avg_buy_price = serializer.data["avg_buy_price"]
        data = {"avg_buy_price":avg_buy_price}
        return Response(data,status=status.HTTP_200_OK)
    
class HoldingView(ListAPIView):
    """ Gives the holding values for a given user id"""
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = HoldingSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Holding.objects.filter(user__id=user_id)
    