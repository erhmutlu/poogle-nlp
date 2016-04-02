from apps.defaultapp.shapers import set_params, filter_by_entity_key

__author__ = 'erhmutlu'


class Movie:

    def get_films_release_soon(self, user_input, intent):
        return self.__return_empty_or_with_amount(intent)

    def get_films_released_already(self, user_input, intent):
        return self.__return_empty_or_with_amount(intent)

    def get_films_released_this_week(self, user_input, intent):
        return set_params({})

    def __return_empty_or_with_amount(self, intent):
        params = intent.get('params')
        amounts = filter_by_entity_key(params, 'ENTITY_KEY_NUMBER')

        params = {}
        if len(amounts) > 0:
            params['amount'] = amounts[0]
        return set_params(params=params)