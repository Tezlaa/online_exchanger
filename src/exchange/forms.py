from typing import Tuple

from django import forms
from django.core.exceptions import ValidationError

from .services.datas import CurrencyInfo


def get_choices(self: CurrencyInfo) -> Tuple[Tuple[str, str], ...]:
    """ Get values for the select field """
    
    result = ()
    full_name_currency = {'UAH': 'UAH        (Гривна)', 'RUB': 'RUB        (Рубль)',
                          'EUR': 'EUR        (Евро)', 'USD': 'USD        (Доллар)',
                          'BYN': 'BYN        (Бел. рубль)', 'PM': 'PM        (Parimatch)',
                          'USDT': 'USDT        (Тезер)', 'BTC': 'BTC        (Bitcoin)',
                          'ETH': 'ETH        (Ethereum)'}

    for name in (currency for currency in self.get_bank().keys()):
        result += ((name, full_name_currency[name]),)
    return result


class OrderInfoForm(forms.Form):
    username = forms.CharField(label='ФИО отправителя',
                               widget=forms.TextInput({'id': 'floatingName_get',
                                                       'class': "form-control form-control-updata",
                                                       'placeholder': "ФИО отправителя кирилицей"}))
    
    binance_wallet_getter = forms.CharField(label='Номер кошелька отправителя', required=False,
                                            widget=forms.TextInput({'class': "form-control form-control-updata trc-form",
                                                                    'placeholder': "Номер кошелька Tether TRC-20",
                                                                    'id': 'binance_wallet_getter'}))
    
    card_number = forms.CharField(label='Номер карты отправителя', required=False,
                                  widget=forms.TextInput({'class': "form-control form-control-updata",
                                                          'placeholder': "Номер карты отправителя",
                                                          'id': 'card_number'}))
    
    number = forms.CharField(label='Номер телефона',
                             widget=forms.TextInput({'id': 'floatingNumber',
                                                     'type': 'tel',
                                                     'class': "form-control form-control-number",
                                                     'placeholder': "Номер телефона для связи"}))

    username_take = forms.CharField(label='ФИО получателя', required=False,
                                    widget=forms.TextInput({'id': 'floatingName_take',
                                                            'class': "form-control form-control-updata",
                                                            'placeholder': "ФИО получателя кирилицей"}))
    
    binance_wallet_taker = forms.CharField(label='Номер кошелька получателя', required=False,
                                           widget=forms.TextInput({'class': "form-control form-control-updata trc-form",
                                                                   'placeholder': "Номер кошелька Tether TRC-20",
                                                                   'id': 'binance_wallet_taker'}))
    
    number_taker = forms.CharField(label='Номер телефона получателя', required=False,
                                   widget=forms.TextInput({'class': 'form-control form-control-updata',
                                                           'placeholder': 'Номер телефона получателя',
                                                           'id': 'floationgNumberTaker',
                                                           'style': 'display: none;'}))
    
    card_number_take = forms.CharField(label='Номер карты получателя', required=False,
                                       widget=forms.TextInput({'class': "form-control form-control-updata",
                                                               'placeholder': "Номер карты получателя",
                                                               'id': 'card_number_take'}))
    
    def clean_number(self):
        number_data = self.cleaned_data.get('number')
        return number_data
    
    def clean_card_number(self):
        card_number_data = self.cleaned_data.get('card_number')
        return card_number_data
    
    def clean_card_number_take(self):
        card_number_take_data = self.cleaned_data.get('card_number_take')
        return card_number_take_data


class TradeForm(forms.Form):
    """ Forms with calculator """
    
    info_class = CurrencyInfo()
    
    currency_name = get_choices(info_class)
    
    currency_get = forms.ChoiceField(choices=currency_name,
                                     widget=forms.Select({'class': 'select_currency',
                                                          'id': 'currency1',
                                                          'onchange': 'updateBankOptions()'}))
    
    currency_take = forms.ChoiceField(choices=currency_name,
                                      widget=forms.Select({'class': 'select_currency',
                                                           'id': 'currency2',
                                                           'onchange': 'updateBankOptions()'}))

    bank_get = forms.CharField(widget=forms.Select({'class': 'select_banks', 'id': 'bank_get'}))
    bank_take = forms.CharField(widget=forms.Select({'class': 'select_banks', 'id': 'bank_take'}))
    
    money_get = forms.FloatField(label='Отдаю',
                                 widget=forms.NumberInput({'class': "input_how_many_get",
                                                           'placeholder': 'Отдаю',
                                                           'id': 'id_money_give',
                                                           'name': 'money_give', }))
    money_take = forms.FloatField(label='Получаю',
                                  widget=forms.NumberInput({'class': "input_how_many_take",
                                                            'placeholder': 'Получаю',
                                                            'id': 'id_money_take',
                                                            'name': 'money_take', }))

    def clean_money_get(self):
        """ Check on valid how mach money get by limit """
        
        currency_get = self.cleaned_data['currency_get']
        money_get = self.cleaned_data['money_get']
        
        limits = self.info_class.get_limits()

        if not limits.get(currency_get):
            return money_get
        
        limit = limits[currency_get]
        
        if limit['min'] <= money_get and limit['max'] >= money_get:
            return money_get
        
        raise ValidationError(f"{currency_get}: мин. {limit['min']}, макс. {limit['max']}")


class MixinFormsAllOfferInfo(TradeForm, OrderInfoForm):
    """ Mixin with two forms, all informations about offer trade """