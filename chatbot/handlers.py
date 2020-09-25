from settings import FLIGHTS_NUMBERS
import re
import datetime

from models import Registration

re_city = re_first_name = re_last_name = re.compile(r'^[\w\-\s\.]{3,40}$')
re_email = re.compile(r"\b^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$\b")
re_phone = re.compile(r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')
re_date = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')


def handle_departure_city(text, context):
    match = re.match(re_city, text)
    if match:
        return city_handle(context, text, direction='departure_city')
    else:
        return False


def handle_arrival_city(text, context):
    match = re.match(re_city, text)
    if match:
        return city_handle(context, text, direction='arrival_city')
    else:
        return False


def city_handle(context, text, direction):
    cities = get_city(text, context)
    if len(cities) < 1:
        return False
    elif len(cities) > 1:
        context['search_warning'] = 'Найдены следующие города:\n'
        for city, code in cities.items():
            context['search_warning'] += city + ' (' + code + ')\n'
        context['search_warning'] += 'Уточните выбор'
        return False
    else:
        context[direction] = cities
        for city, code in cities.items():
            context['city_message'] = city + ' (' + code + ')'
        if direction == 'departure_city':
            context['departure_city_to_print'] = context['city_message']
        else:
            context['arrival_city_to_print'] = context['city_message']
        context['city_message'] = 'Принято:\n' + context['city_message'] + '\n'
        return True


def get_city(search_str, context):
    search_str = search_str.lower()
    cities = {}
    for city in context['cities_json']:
        if (city['name'] and city['name'].lower().find(search_str) > -1) or \
                (city['cases']['vi'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                (city['cases']['tv'] and city['cases']['tv'].lower().find(search_str) > -1) or \
                (city['cases']['ro'] and city['cases']['ro'].lower().find(search_str) > -1) or \
                (city['cases']['pr'] and city['cases']['pr'].lower().find(search_str) > -1) or \
                (city['cases']['da'] and city['cases']['da'].lower().find(search_str) > -1) or \
                city['code'].lower() == search_str:
            cities[city['name']] = city['code']
    return cities


def handle_date(text, context):
    match = re.match(re_date, text)
    if match:
        departure_date = datetime.date(day=int(text[:2]), month=int(text[3:5]), year=int(text[6:10]))
        if departure_date < datetime.date.today():
            context['search_warning'] = 'Невозможно найти билет на прошедшую дату'
            return False
        if departure_date > datetime.date.today() + datetime.timedelta(365):
            context['search_warning'] = 'Не можем искать билет более, чем на год вперёд'
            return False
        context['date'] = text
        return True
    else:
        return False


def handle_flight(text, context):
    if text.isdigit() and 0 < int(text) <= context['flights_found']:
        context['date_flight_to_print'] = context['date_flight' + str(text)]
        context['time_flight_to_print'] = context['time_flight' + str(text)]
        context['flight_to_print'] = context['thread' + str(text)]
        return True
    else:
        context['flight_to_print'] = None
        return False


def handle_seats(text, context):
    if text.isdigit() and 0 < int(text) < 6:
        context['seats'] = text
        return True
    else:
        return False


def handle_comment(text, context):
    if 0 < len(text) < 500:
        context['comment'] = text
        return True
    else:
        return False


def handle_confirm(text, context):
    if text.lower().find('yes') > -1 or text.lower().find('да') > -1:
        context['confirm'] = True
        return True
    else:
        return False


def handle_first_name(text, context):
    match = re.match(re_first_name, text)
    if match:
        context['first_name'] = text
        return True
    else:
        return False


def handle_last_name(text, context):
    match = re.match(re_last_name, text)
    if match:
        context['last_name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False


def handle_phone(text, context):
    match = re.match(re_phone, text)
    if match:
        context['phone'] = text
        return True
    else:
        return False
