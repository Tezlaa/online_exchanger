from rest_framework.response import Response

from rest_framework.views import APIView

from bot.urils.decorators import token_valid
from exchange.services.P2Pparser.parsers_rate import ParseRate
from exchange.models import Currency


class ParseP2PRateAPI(APIView):
    """API for get rate with BinanceP2P API
    
    Methods:
        get: getting by one currency pair
            Example:
                ?buy=UAH&sell=RUB
        post: getting by json
            Example:
                [
                    {
                        "buy": "UAH",
                        "sell": "RUB"
                    },
                    ...
                ]
    """
    
    @token_valid
    def get(self, request):
        data = request.query_params
        currency = [[data.get('buy'), data.get('sell')]]
        
        parse_rate = ParseRate(currency)
        parse_rate.requestP2P()
        
        return Response(parse_rate.request_list)
    
    @token_valid
    def post(self, request):
        data = request.data
        currency_list = [[pair['buy'], pair['sell']] for pair in data]
        
        parse_rate = ParseRate(currency_list)
        parse_rate.requestP2P()
        
        return Response(parse_rate.request_list)
    

class GetAvailableBanksAPI(APIView):
    """ Get the names currency and his banks """
    
    def get(self, request, *args, **kwarks):
        queryset = Currency.objects.prefetch_related('his_banks')
        
        json = {}
        for currency in queryset:
            banks = [{'name': bank.bank_name} for bank in currency.his_banks.all()]
            json[currency.currency] = banks

        return Response(json)
