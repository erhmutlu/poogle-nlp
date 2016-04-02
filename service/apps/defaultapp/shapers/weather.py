from datetime import datetime
from apps.defaultapp.shapers.shaper_helper import filter_by_entity_key, append_resp_with_action_name, sort_params, \
    set_params
from apps.defaultapp.tools.str import to_two_digit_num, find_index_of_word, erase_extra_whitespaces

__author__ = 'erhmutlu'


class Weather:

    def get_weather_by_city(self, user_input, intent):
        params = intent.get('params')

        cities = filter_by_entity_key(params, 'ENTITY_KEY_CITY')
        if len(cities) == 1:
            city = cities[0]
            p = {
                'city': city
            }
            params = set_params(params=p)
            return params
        raise EnvironmentError('1 city is needed but given %s city' % len(cities))

    def get_weather_by_city_hour(self, user_input, intent):
        params = sort_params(user_input, intent.get('params'))

        cities = filter_by_entity_key(params, 'ENTITY_KEY_CITY')
        hours = filter_by_entity_key(params, 'ENTITY_KEY_NUMBER')
        if len(cities) == 1 and len(hours) in range(1,3):
            now = datetime.now()
            curr_date = self.__make_date_str(now.day, now.month)

            hour_str = self.__make_hour_str(hours)
            city = cities[0]

            p = {
                'hour': hour_str,
                'city': city,
                'date': curr_date
            }

            params = set_params(params=p)
            return append_resp_with_action_name(params, 'get_weather_by_city_date_hour')
        else:
            raise EnvironmentError('1 city and 1 <= hour <= 2 needed but given %s city %s hour' % (len(cities), len(hours)))

    def get_weather_by_city_date(self, user_input, intent):
        params = sort_params(user_input, intent.get('params'))

        cities = filter_by_entity_key(params, 'ENTITY_KEY_CITY')
        days = filter_by_entity_key(params, 'ENTITY_KEY_NUMBER')
        months = filter_by_entity_key(params, 'ENTITY_KEY_MONTH')
        if len(cities) == 1 and len(days) == 1 and len(months) == 1:
            city = cities[0]
            day = days[0]
            month = months[0]

            date = self.__make_date_str(day['value'], month['value'])

            p = {
                'city': city,
                'date': date
            }

            params = set_params(params=p)
            return params
        else:
            raise EnvironmentError('1 city and 1 day and 1 month needed but given %s city %s day %s month' % (len(cities), len(days), len(months)))

    def get_weather_by_city_date_hour(self, user_input, intent):
        params = sort_params(user_input, intent.get('params'))

        cities = filter_by_entity_key(params, 'ENTITY_KEY_CITY')
        numbers = filter_by_entity_key(params, 'ENTITY_KEY_NUMBER')
        months = filter_by_entity_key(params, 'ENTITY_KEY_MONTH')

        if not len(months) == 1:
           raise EnvironmentError('1 month needed but given %s month'
                                   % len(months))

        month = months[0]
        user_input = erase_extra_whitespaces(user_input)
        hours = []
        days = []

        for number in numbers:
            str = '%s %s' % (number['presentation_value'], month['presentation_value'])
            if len(days) == 0 and find_index_of_word(user_input, str) >= 0:
                days.append(number)
            else:
                hours.append(number)

        if len(cities) == 1 and len(hours) in range(1, 3) and len(days) == 1:
            city = cities[0]
            day = days[0]
            date_str = self.__make_date_str(day['value'], month['value'])
            hour_str = self.__make_hour_str(hours)

            p = {
                'date': date_str,
                'hour': hour_str,
                'city': city
            }

            params = set_params(params=p)
            return params
        else:
            raise EnvironmentError('1 city and 1 <= hour <= 2 and 1 month and 1 days needed but given %s city %s hour %s day'
                                   % (len(cities), len(numbers), len(days)))

    def __make_hour_str(self, hours):
        h = [to_two_digit_num(dict['value']) for dict in hours]
        if len(h) ==1:
            h.append('00')
        return ':'.join(h)

    def __make_date_str(self, day, month):
        now = datetime.now()
        year = str(now.year)

        two_digit_day = to_two_digit_num(day)
        two_digit_month = to_two_digit_num(month)

        d = [year, two_digit_month, two_digit_day]

        return '-'.join(d)