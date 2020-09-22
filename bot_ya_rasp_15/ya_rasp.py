import requests
try:
    from settings import YA_TOKEN, YA_URL
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
import logging
log = logging.getLogger('bot')


def request_ya_rasp(date, from_station, request, to_station, request_flights):
    try:
        request = requests.get(YA_URL + 'apikey=' + YA_TOKEN +
                               '&format=json&transport_types=plane&system=iata&transfers=false&lang=ru_RU&limit='
                               + request_flights + '&from=' + from_station + '&to=' + to_station + '&date=' + date)
    except Exception:
        log.exception('Ошибка запроса Яндекс-Расписания')
    return request.text
