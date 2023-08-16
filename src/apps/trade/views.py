from typing import Any, Dict

from django.views.generic import TemplateView

from apps.trade.utils.decorator import valid_open_order


class WaitingAdminCard(TemplateView):
    template_name = 'trade/waiting_card.html'
    
    @valid_open_order()
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contexts = super().get_context_data(**kwargs)
        contexts['currency_get'] = contexts['object_database'].order.currency_get
        return contexts
    

class SuccessfulTrade(TemplateView):
    template_name = 'trade/successful_trade.html'
    
    @valid_open_order()
    def get_context_data(self, **kwarks: Any) -> Dict[str, Any]:
        contexts = super().get_context_data(**kwarks)
        
        contexts['id_order'] = contexts['object_database'].order.id_order
        contexts['money_get'] = contexts['object_database'].order.how_many_get
        contexts['currency'] = contexts['object_database'].order.currency_get
        
        contexts['object_database'].delete()
        
        return contexts