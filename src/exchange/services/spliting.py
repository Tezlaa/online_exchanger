from typing import Any, Dict


def split_form_data_in_order_model(id_order: int, **kwarks: dict) -> Dict[str, Any]:
    return {'id_order': id_order,
            'currency_get': kwarks['currency_get'],
            'currency_take': kwarks['currency_take'],
            'bank_get': kwarks['bank_get'],
            'bank_take': kwarks['bank_take'],
            'how_many_get': kwarks['money_get'],
            'how_many_take': kwarks['money_take'],
            'name_geter': kwarks['username'],
            'card_geter': kwarks['card_number'],
            'number_getter': kwarks['number'],
            'name_taker': kwarks['username_take'],
            'number_taker': kwarks['number_taker'],
            'card_taker': kwarks['card_number_take']}
