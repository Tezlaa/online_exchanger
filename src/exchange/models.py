import logging
import subprocess
import sys

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from django.conf import settings


class Currency(models.Model):
    """Currency to trade, select many to many banks and limits"""
    
    currency = models.CharField(max_length=10, verbose_name='Название валюты')
    
    his_banks = models.ManyToManyField(to='Banks', verbose_name='Банки')

    min_value = models.PositiveIntegerField(verbose_name="Минимальная цена", blank=True, default=1)
    max_value = models.PositiveIntegerField(verbose_name='Максимальная цена', blank=True, default=10**6)
    
    def get_his_banks(self):
        return ", ".join([bank['bank_name'] for bank in self.his_banks.all().values('bank_name')])

    def __str__(self) -> str:
        return self.currency

    class Meta:
        verbose_name = 'Валюта для обмена'
        verbose_name_plural = 'Валюты для обмена'


class Banks(models.Model):
    """Creating banks for currency and his limit"""
      
    bank_name = models.CharField(max_length=255, verbose_name='Банк')
    limit_bank = models.PositiveIntegerField(verbose_name='Лимит для банка', blank=True, default=10**6)
    
    def __str__(self) -> str:
        return self.bank_name

    class Meta:
        verbose_name = 'Банк для обмена'
        verbose_name_plural = 'Банки для обмена'
    
    
class FactorPrice(models.Model):
    """Factor for price rate and calculate"""
    
    fiat_buy = models.CharField(max_length=255, verbose_name='Валюта покупки')
    fiat_sell = models.CharField(max_length=255, verbose_name='Валюта продажи')
    factor_buy = models.FloatField(verbose_name='Множитель покупки')
    factor_sell = models.FloatField(verbose_name='Множитель продажи')
    
    class Meta:
        verbose_name = 'Множитель'
        verbose_name_plural = 'Множитель'
    
    def __str__(self):
        return f'{self.fiat_buy}/{self.fiat_sell}'


class SettingUpWebSite(models.Model):
    """Customizing different site settings"""
    
    visible_parimatch = models.BooleanField(verbose_name='Видимость париматч')
    link_tg = models.CharField(verbose_name='Ссылка на телеграм', max_length=255)
    number_viber = models.CharField(verbose_name='Номер Viber (без "+" в начале)', max_length=255)
    link_whatsapp = models.CharField(verbose_name='Ссылка на WhatsApp', max_length=255)
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'


class OffersData(models.Model):
    """All offer in the exchange"""
    
    id_order = models.IntegerField(unique=True, verbose_name='ID заявки')
    
    time_create = models.DateTimeField(auto_now_add=True)
    
    currency_get = models.CharField(max_length=255, verbose_name='Отдаёт валюту')
    currency_take = models.CharField(max_length=255, verbose_name='Получает валюту')
    
    bank_get = models.CharField(max_length=255, verbose_name='С банка')
    bank_take = models.CharField(max_length=255, verbose_name='В банк')
    
    how_many_get = models.CharField(max_length=255, verbose_name='Отдаёт')
    how_many_take = models.CharField(max_length=255, verbose_name='Получает')
    
    name_geter = models.CharField(max_length=255, verbose_name='ФИО отправителя')
    card_geter = models.CharField(max_length=255, verbose_name='Карта отправителя')
    
    number_getter = models.CharField(max_length=255, verbose_name='Номер отправителя')
    
    name_taker = models.CharField(max_length=255, verbose_name='ФИО получателя')
    number_taker = models.CharField(max_length=255, verbose_name='Номер получателя')
    card_taker = models.CharField(max_length=255, verbose_name='Карта получателя')
    
    card_admin = models.CharField(max_length=255, blank=True, null=True, verbose_name='Карта администратора')
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def __str__(self):
        return f'id order:{self.id_order}, name: {self.name_geter}'


@receiver([post_save, post_delete], sender=SettingUpWebSite)
@receiver([post_save, post_delete], sender=FactorPrice)
@receiver([post_save, post_delete], sender=Currency)
@receiver([post_save, post_delete], sender=Banks)
def clear_cache(sender, **kwraks):
    """
    Deleting the cache after update database
    """
    cache.clear()
    logging.info('cache update')