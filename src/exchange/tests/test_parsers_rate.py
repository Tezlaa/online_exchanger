from django.test import TestCase

from exchange.services.P2Pparser.parsers_rate import ParseRate


class ParsersTestCase(TestCase):
    
    def test_request_list(self):
        currency_list = [
            ["RUB", "UAH"], ['BYN', 'UAH'], ["USD", "UAH"], ["EUR", "UAH"],
            ["USDT", "UAH"], ["BTC", "UAH"], ["ETH", "UAH"], ["USDT", "PM"],
        ]
        
        tests = ParseRate(currency_list)
        self.assertEqual('RUB', tests.request_list[0]['sell'])
        self.assertEqual(len(currency_list), len(tests.request_list) / 2)