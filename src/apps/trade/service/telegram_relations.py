import asyncio

import aiohttp
import requests

from django.conf import settings


async def request_telegram(id_order: int) -> dict:
        
    async with aiohttp.ClientSession() as session:
        task = session.get(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates')
        response = await asyncio.gather(task)
    
        json_request = await response[0].json()
    
    response = {'status': 'empty'}
    for message in json_request['result']:
        try:
            reply_text = message['channel_post']['reply_to_message']['text']
            reply_id = int((reply_text.split('\n\n')[0]).split('ID: ')[1])
            if reply_id == id_order:
                answer_card = message['channel_post']['text']
                response = {'status': 'ok', 'response': answer_card}
                break
        except KeyError:
            pass
        except IndexError:
            pass
    
    return response


def send_offer_in_admin_chat(info_data: dict) -> None:
    message_admin = (f'ID: ***{info_data["id_order"]}***\n\n'
                     f'Валюта отпраки: ***{info_data["currency_get"]}***\n'
                     f'Валюта получения: ***{info_data["currency_take"]}***\n'
                     f'Банк отправки: {info_data["bank_get"]}\n'
                     f'Банк получения: {info_data["bank_take"]}\n'
                     f'Сумма отправки: `{info_data["how_many_get"]}`\n'
                     f'Сумма получения: `{info_data["how_many_take"]}`\n'
                     f'Имя отправителя: `{info_data["name_geter"]}`\n'
                     f'Карта отправителя: `{info_data["card_geter"]}`\n'
                     f'Номер отправителя : `{info_data["number_getter"]}`\n'
                     f'Имя получателя: `{info_data["name_taker"]}`\n'
                     f'Номер получателя: `{info_data["number_taker"]}`\n'
                     f'Карта получателя: `{info_data["card_taker"]}`')
    requests.get(url=f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
                 data={"chat_id": settings.CHAT_ID,
                       "text": str(message_admin),
                       "parse_mode": "MARKDOWN", })