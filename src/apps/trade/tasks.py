import requests

from celery import shared_task

from django.conf import settings


@shared_task
def send_photo_to_telegram(photo) -> None:
    requests.post(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendPhoto',
                  data={
                      'chat_id': settings.CHAT_ID},
                  files={
                      'photo': ('image.jpg', photo)})


@shared_task
def send_message_to_telegram(message: str) -> None:
    requests.get(url=f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
                 data={"chat_id": settings.CHAT_ID,
                       "text": message,
                       "parse_mode": "MARKDOWN", })
    