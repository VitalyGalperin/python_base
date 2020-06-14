import re

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_city = re.compile(r'^[\w\-\s\.]{3,40}$')
re_email = re.compile(r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$')
re_phone = re.compile(r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')
re_date = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')

def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    match = re.match(re_email, text)
    if match:
        context['email'] = text
        return True
    else:
        return False


def handle_departure_city(text, context):
    match = re.match(re_city, text)
    if match:
        context['departure_city'] = text
        return True
    else:
        return False


def handle_arrival_city(text, context):
    match = re.match(re_city, text)
    if match:
        context['arrival_city'] = text
        return True
    else:
        return False
