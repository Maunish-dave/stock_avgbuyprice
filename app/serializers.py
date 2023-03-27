
from rest_framework import serializers
from .models import StockActions, SplitAction, Holding, User


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


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ( "id", "username", "password", )