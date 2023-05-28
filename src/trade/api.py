import asyncio
import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from trade.models import OffersData
from trade.utils.decorator import valid_open_order
from trade.service.telegram_relations import request_telegram


class ResponseAdminTelegram(APIView):
    
    @valid_open_order(id_in_link=False)
    def get(self, request):
        id_order = int(request.GET['id_order'])
        response = asyncio.run(request_telegram(id_order))

        if response['status'] == 'ok':
            OffersData.objects.filter(id_order=id_order).update(card_admin=response['response'])

        return Response(response)
    

class SendPhotoAdminTelegram(APIView):
    
    @valid_open_order(id_in_link=False)
    def post(self, request):
        photo_file = request.FILES['photo']
        photo_content = photo_file.read()
        photo_file.close()  # Close the file to free up resources

        requests.post(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto',
                      data={
                          'chat_id': settings.CHAT_ID},
                      files={
                          'photo': ('image.jpg', photo_content)})

        return Response({'success': True})


class SendLeaveAdminTelegram(APIView):
    
    @valid_open_order()
    def get(self, request, id_order, object_database):
        message = request.GET['message']

        requests.get(url=f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
                     data={"chat_id": settings.CHAT_ID,
                           "text": message,
                           "parse_mode": "MARKDOWN", })
        object_database.delete()
        return Response({'success': True})