from django.urls import path

from apps.exchange.views import ExchangeMainPage
from apps.exchange.api import ParseP2PRateAPI, GetAvailableBanksAPI


urlpatterns = [
    path('', ExchangeMainPage.as_view(), name='main_page'),

    # API
    path('api/v1/getPrice', ParseP2PRateAPI.as_view()),
    path('api/v1/getBanks', GetAvailableBanksAPI.as_view())
]