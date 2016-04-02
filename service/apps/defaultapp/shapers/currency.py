from apps.defaultapp.shapers.shaper_helper import filter_by_entity_key, sort_params, set_params

__author__ = 'erhmutlu'


class Currency:

    def convert_currency_units(self, user_input, intent):
        params = sort_params(user_input, intent.get('params'))

        currencies = filter_by_entity_key(params, 'ENTITY_KEY_CURRENCY')
        amounts = filter_by_entity_key(params, 'ENTITY_KEY_NUMBER')

        if len(currencies) == 2 and len(amounts) == 1:
            from_currency = currencies[0]
            to_currency = currencies[1]
            amount = amounts[0]
            p = {
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
            }

            return set_params(params=p)
        raise EnvironmentError('2 currency, 1 amount is needed but given %s currency %s amount' % (len(currencies), len(amounts)))