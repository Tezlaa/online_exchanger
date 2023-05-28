import random
from typing import Any
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from exchange.models import OffersData
from exchange.services.P2Pparser.parsers_rate import ParseRate
from exchange.services.spliting import split_form_data_in_order_model
from exchange.forms import MixinFormsAllOfferInfo

from trade.models import OpenOrder
from trade.service.telegram_relations import send_offer_in_admin_chat


class ExchangeMainPage(FormView):
    """ Base view """
    
    template_name = 'exchange/index.html'
    form_class = MixinFormsAllOfferInfo
    success_url = reverse_lazy('waiting_admin_card')
    
    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        
        currency_list = [
            ["RUB", "UAH"], ['BYN', 'UAH'], ["USD", "UAH"], ["EUR", "UAH"],
            ["USDT", "UAH"], ["BTC", "UAH"], ["ETH", "UAH"], ["USDT", "PM"],
        ]
        p2p_rate = ParseRate.get_rate(currency_list)
        for context in p2p_rate.items():
            contexts[context[0]] = context[1]

        return contexts
    
    def form_valid(self, form: Any):
        form_data = form.cleaned_data
        
        if not form.is_valid():
            return reverse_lazy('main_page')
        
        id_order = random.randint(10000, 100000)
        nessasary_data_format = split_form_data_in_order_model(id_order, **form_data)
        
        OpenOrder.objects.create(order=OffersData.objects.create(**nessasary_data_format))
        send_offer_in_admin_chat(nessasary_data_format)
        
        return redirect(to=reverse(
            viewname='waiting_admin_card',
            args=(id_order,
                  str(form_data["money_get"]),
                  form_data['currency_get'] if form_data['currency_get'] != 'PM' else 'USDT')))
