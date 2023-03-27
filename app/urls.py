from django.urls import path
from .views import Home, StockActionView, AvgBuyPriceView, SplitActionView, HoldingView, CreateUserView

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('avg_buy_price/<int:user_id>/',AvgBuyPriceView.as_view(),name='avg_buy_price'),
    path('stock_action/<int:user_id>/', StockActionView.as_view(), name='stock_action'),
    path('split_action/<int:user_id>/', SplitActionView.as_view(), name='split_action'),
    path('holdings/<int:user_id>/', HoldingView.as_view(), name='holdings'),
    path('create/',CreateUserView.as_view(),name='create')
]