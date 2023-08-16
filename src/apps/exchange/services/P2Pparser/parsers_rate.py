import logging
import time
import copy
import asyncio

from typing import TypedDict, Dict, List

from django.db.models import QuerySet

import aiohttp
import fake_useragent

from apps.exchange.models import FactorPrice


class RequestList(TypedDict):
    trade_type: str
    currency_type: str
    pair: list
    buy: str
    sell: str
    currency_to_usdt: Dict[str, list]
    price: float


class SetingUpForParsing:
    all_crypto = ['BTC', 'ETH', 'BNB',
                  'ADA', 'XRP', 'SOL',
                  'DOT', 'USDT', 'DOGE',
                  'AVAX', 'BUSD', 'LUNA']
    
    unusual_currency = {'PM': 'UAH'}
    
    def __init__(self, currency_list: List[List[str]]):
        self.currency_list = currency_list
        self.request_list: List[RequestList] = []
        
    def _split_currency(self):
        """Split currency in request format.
        
        request_list = [
            trade_type(str): BUY/SELL
            currency_type(str): FIAT/CRYPTO
            pair(list): Exemple: ['UAH','RUB']
            buy(str): currency that need to buy
                Example: UAH/RUB need to buy -> RUB
            sell(str): currency that need to sell
            currency_to_usdt(dict{str: list[str, str, int]}):
                                    if in pair is not crypto than:
                                        Example: UAH/RUB -> {'UAH': ['USDT', 'UAH', 0],
                                                             'RUB': ['USDT', 'RUB', 0],}
                                    else:
                                        {'UAH': ['BTC', 'UAH', 0]}
                                    index 3 this price before request in API, defoult=0
            price(int): price on this pair, defoult=0
        ]
        """
        for pair in self.currency_list:
            trade_type = 'BUY'
            buy = pair[1]
            sell = pair[0]
            price = 0
        
            if pair[0] in self.all_crypto or pair[1] in self.all_crypto:
                currency_type = 'CRYPTO'
                if self.unusual_currency.get(buy):
                    buy_name = self.unusual_currency[buy]
                    sell_name = buy
                else:
                    buy_name, sell_name = buy, sell
                currency_to_usdt = {sell_name: [sell, buy_name, 0]}
            else:
                currency_type = 'FIAT'
                currency_to_usdt = {sell: ['USDT', sell, 0],
                                    buy: ['USDT', buy, 0]}
            
            self.request_list.append({'trade_type': trade_type,
                                      'currency_type': currency_type,
                                      'pair': pair,
                                      'buy': buy,
                                      'sell': sell,
                                      'currency_to_usdt': currency_to_usdt,
                                      'price': price})
            
        for sell_pair in self.__copy_in_sell_pair(self.request_list):
            self.request_list.append(sell_pair)

    def __copy_in_sell_pair(self, list_with_request: list) -> list:
        """copy list and remake trade type on 'SELL', reversed pair and buy with sell

        Args:
            list_with_request (list): list for copy

        Returns:
            list: result list
        """
        
        result = []
        copy_data = copy.deepcopy(list_with_request)

        for i, pair in enumerate(copy_data):
            copy_data[i]['trade_type'] = 'SELL'
            copy_data[i]['pair'] = list(reversed(pair['pair']))
            copy_data[i]['buy'], copy_data[i]['sell'] = copy_data[i]['sell'], copy_data[i]['buy']
            
            result.append(copy_data[i])
        return result


class ParseRate(SetingUpForParsing):
    """Parse rete of currency, parsing with api Binance P2P

    Args:
        currency_list (List[List[str]]): Your currency list, where the
            first currency is a buy and the second currency is a sell.
            Example: [['UAH', 'RUB'], [...], ...]
    """
    
    def __init__(self, currency_list: List[List[str]]):
        super().__init__(currency_list)
        self._split_currency()
        
    @classmethod
    def get_rate(cls, currency_list: List[List[str]]) -> Dict[str, List[dict]]:
        """ Get rate for the frontend.
        
        Args:
            ParseRate all his args

        Return:
            (Dict[str, List[dict]]): result dict where keys is (rate_buy, rate_sell
                                                                rate_buy_pm, rate_sell_pm)
            and values is List[dict] where dict is pair name and price
               symbol1(str): buy currency
               symbol2(str): sell currency
               price(int): price before requestP2P
        """
        
        self = cls(currency_list)
        self.requestP2P()
        
        return self.get_raw_rate()
        
    def requestP2P(self):
        url_api = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
        asyncio.run(self.__create_request_tasks(url_api, self.request_list))
        self.__calculate_price()
    
    def get_raw_rate(self) -> Dict[str, List[dict]]:
        """
        Getting rate for the template
        
        Return:
            (Dict[str, List[dict]]): result dict where keys is (rate_buy, rate_sell
                                                                rate_buy_pm, rate_sell_pm)
            and values is List[dict] where dict is pair name and price
               symbol1(str): buy currency
               symbol2(str): sell currency
               price(int): price before requestP2P
        """
        
        result = {'rate_buy': [], 'rate_sell': [],
                  'rate_buy_pm': [], 'rate_sell_pm': []}
        
        for pair_data in self.request_list:
            if pair_data['trade_type'] == 'BUY':
                path = 'rate_buy'
            else:
                path = 'rate_sell'
            
            if pair_data['buy'] == 'PM' or pair_data['sell'] == 'PM':
                path = path + '_pm'
            
            result[path].append({'symbol1': pair_data['sell'],
                                 'symbol2': pair_data['buy'],
                                 'price': pair_data['price']})
        
        return result

    async def __create_request_tasks(self, url_api: str, request_dict: List[RequestList]):
        async with aiohttp.ClientSession() as session:
            tasks = {'tradeType': {'BUY': {}, 'SELL': {}}}
            for pair_dict in request_dict:
                for currency in pair_dict['currency_to_usdt'].items():
                    json_data = {
                        'page': 1,
                        'rows': 1,
                        'asset': '',
                        'fiat': '',
                        'tradeType': '',
                    }
                    json_data['tradeType'] = pair_dict['trade_type']
                    json_data['asset'] = currency[1][0]
                    json_data['fiat'] = currency[1][1]
                    
                    pair = f"{json_data['fiat']}/{json_data['asset']}"
                    try:
                        tasks['tradeType'][json_data['tradeType']][pair]
                    except KeyError:
                        headers = {'user-agent': fake_useragent.UserAgent().random}
                        
                        tasks['tradeType'][json_data['tradeType']][pair] = session.post(url=url_api,
                                                                                        json=json_data,
                                                                                        headers=headers)
            time_start = time.time()
            responses = await asyncio.gather(*self.__task_dict_in_list(tasks))
            print('request time: ', time.time() - time_start)
            
            for response in responses:
                response_json = await response.json()
                try:
                    response_json = response_json['data'][0]['adv']
                    self.__set_price_pair(response_json)
                except Exception:
                    logging.warning(await response.json())

    def __calculate_price(self):
        """Set price in list with all pair"""
        all_factor = self.__get_all_factor()
        too_long_crypto = ['BTC', 'ETH']
        
        for pair_data in self.request_list:
            sell = pair_data['sell']
            buy = pair_data['buy']
            trade_type = pair_data['trade_type']
            
            factor = self.get_factor(all_factor, trade_type, buy, sell)
            formats = '%.2f' if sell not in too_long_crypto and buy not in too_long_crypto else '%.7f'
            
            try:
                price_sell = pair_data['currency_to_usdt'][sell][2]
            except KeyError:
                price_sell = pair_data['currency_to_usdt'][buy][2]

            try:
                price_buy = pair_data['currency_to_usdt'][buy][2]
            except KeyError:
                price_buy = pair_data['currency_to_usdt'][sell][2]
                
            if pair_data['currency_type'] == 'FIAT':
                price = self.__get_price_fiat(price_sell, price_buy)
            else:
                price = self.__get_price_crypto(price_sell, trade_type)
                
            pair_data['price'] = float(formats % (price * factor))
    
    def __get_all_factor(self) -> QuerySet:
        """Getting all coefficient for a currency"""
        all_factor = FactorPrice.objects.all()
        return all_factor
    
    def get_factor(self, factor: QuerySet, trade_type: str, buy_name: str, sell_name: str) -> float:
        for pair in factor:
            buy_name_db = pair.fiat_buy
            sell_name_db = pair.fiat_sell
            
            comparison_first = (buy_name_db == buy_name and sell_name_db == sell_name)
            comparison_second = (buy_name_db == sell_name and sell_name_db == buy_name)
            
            if comparison_first or comparison_second:
                if trade_type == 'SELL':
                    return float(pair.factor_sell)
                return float(pair.factor_buy)
        return 1
    
    def __set_price_pair(self, response: dict) -> None:
        """Set in request_list price"""
        
        response_pair = [response['asset'], response['fiatUnit']]
        for pair_dict in self.request_list:
            for currency in pair_dict['currency_to_usdt'].items():
                if response_pair == currency[1][0:2] and response['tradeType'] == pair_dict['trade_type']:
                    currency[1][2] = float(response['price'])
                    break

    def __task_dict_in_list(self, dict: Dict[str, Dict[str, dict]]) -> list:
        list_tasks = []
        
        for trade_type in dict['tradeType'].values():
            for task in trade_type.values():
                list_tasks.append(task)

        return list_tasks

    def __get_price_fiat(self, sell_price: float, buy_price: float) -> float:
        return float(buy_price / sell_price)
    
    def __get_price_crypto(self, sell_price: float, trade_type: str) -> float:
        price_crypto = sell_price
             
        if trade_type == 'SELL':
            price_crypto = 1 / price_crypto
        
        return price_crypto