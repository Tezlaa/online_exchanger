from django.urls import path

from .views import WaitingAdminCard, SuccessfulTrade
from .api import (
    ResponseAdminTelegram,
    SendPhotoAdminTelegram,
    SendLeaveAdminTelegram,
)


urlapi = [
    path('api/v1/responseTelegram', ResponseAdminTelegram.as_view()),
    path('api/v1/sendPhoto', SendPhotoAdminTelegram.as_view()),
    path('api/v1/sendLeave/<int:id_order>', SendLeaveAdminTelegram.as_view()),
]

urlpatterns = [
    path('trade/<int:id_order>/<str:money_get>/<str:currency>/', WaitingAdminCard.as_view(), name='waiting_admin_card'),
    path('trade/successful_trade/<int:id_order>', SuccessfulTrade.as_view(), name='successful_trade'),
    *urlapi
]