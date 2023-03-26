
from rest_framework import serializers
from .models import StockActions, SplitAction, Holding


class StockaActionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StockActions
        fields = [
                  'id',
                  'trade_type',
                  'quantity',
                  'price']

class SpiltActionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SplitAction
        fields = [
                  'id',
                  'ratio']


class HoldingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Holding
        fields = [
                  'id',
                  'quantity',
                  'amount_invested',
                  'avg_buy_price']