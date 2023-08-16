from django.db import models

from apps.exchange.models import OffersData


class OpenOrder(models.Model):
    """All open order in the exchange"""
    
    order = models.ForeignKey(OffersData, on_delete=models.CASCADE, verbose_name='Номер обмена')
    
    class Meta:
        verbose_name = 'Открытая заяка на обмен'
        verbose_name_plural = 'Открытые заявки на обмен'
    
    def __str__(self):
        return f'{self.order}'
