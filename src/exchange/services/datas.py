from typing import Dict, Self

from django.db.models.query import QuerySet

from exchange.models import Currency, Banks


class ORMrequests:
    def _get_info_queryset(self) -> QuerySet:
        data = Currency.objects.select_related('his_banks').values(
            'currency', 'min_value', 'max_value', 'his_banks__bank_name'
        )
        return data  # type: ignore


class CurrencyInfo(ORMrequests):
    def __init__(self) -> None:
        self.queryset = super()._get_info_queryset()

    def get_bank(self) -> Dict[str, str]:
        result = {}
        for queryset in self.queryset:
            currency = queryset['currency']
            bank_name = queryset['his_banks__bank_name']
            
            try:
                result[currency].append(bank_name)
            except KeyError:
                result[currency] = [bank_name]
                
        return result
    
    def get_limits(self) -> Dict[str, Dict[str, int]]:
        result = {}
        for queryset in self.queryset:
            result[queryset['currency']] = {'max': queryset['max_value'],
                                            'min': queryset['min_value']}
        return result
