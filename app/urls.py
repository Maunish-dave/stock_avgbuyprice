from django.urls import path
from .views import Home, StockActionView, AvgBuyPriceView, SplitActionView

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('avg_buy_price/',AvgBuyPriceView.as_view(),name='avg_buy_price'),
    path('stock_action/', StockActionView.as_view(), name='stock_action'),
    path('split_action/', SplitActionView.as_view(), name='split_action'),
]