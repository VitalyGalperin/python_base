import re

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$')
re_phone = re.compile(r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')


def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = text
        return True
    else:
        return False


def handle_departure_city(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['departure_city'] = text
        return True
    else:
        return False


def handle_arrival_city(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['arrival_city'] = text
        return True
    else:
        return False
