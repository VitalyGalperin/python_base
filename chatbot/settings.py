GROUP_ID = 194114072
TOKEN = '6f29220c9eba6519f7b048cd0398e0bcaae4419a30e477daddda01abee415a2bcd2b2813dd52bd7d32b0f'
YA_TOKEN = 'fc086f98-3349-42c6-b490-9b34bc85d83c'
YA_URL = 'https://api.rasp.yandex.net/v3.0/search/?'


DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='q',
    host='localhost',
    database='vk_chat_bot'
    )

SEARCH_PERIOD = 180
FLIGHTS_DAYS = 7
FLIGHTS_NUMBERS = 5
HELLO_MESSAGE = 'Вас приветствует Бот по заказу Авиабилетов!\n' \
                'Для начала заказа билета:     наберите /ticket\n' \
                'Для получения подробной справки:     наберите /help'
HELP_MESSAGE = 'Бот для заказа Авиабилетов\n ' \
               'Для начала заказа билета наберите /ticket , далее следуйте указаниям бота\n'

DEFAULT_ANSWER = 'Не знаю как ответить'

INTENTS = [
    {
        'name': 'Приветствие',
        'tokens': ('hello', 'hi', 'good', 'здрав', 'добр', 'привет',),
        'scenario': None,
        'answer': HELLO_MESSAGE
    },
    {
        'name': 'Помощь',
        'tokens': ('/help', 'помощь', 'помог'),
        'scenario': None,
        'answer': HELP_MESSAGE
    },
    {
        'name': 'Регистрация',
        'tokens': ('/ticket', 'билет', 'заказ', 'закаж'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите название или код города отправления:',
                'failure_text': 'Попробуйте снова ввести название или код города. ',
                'handler': 'handle_departure_city',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите название или код города прибытия:',
                'failure_text': 'Попробуйте снова',
                'handler': 'handle_arrival_city',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Ведите дату выдета (DD-MM-YYYY):',
                'failure_text': 'Неправильный ввод даты, попробуйте еще раз',
                'handler': 'handle_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Выберите порядковый номер рейса из списка:',
                'failure_text': 'Некорректный номер, попробуйте снова',
                'handler': 'handle_flight',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Введите количество мест (от 1 до 5):',
                'failure_text': 'Некорректное количество, попробуйте снова',
                'handler': 'handle_seats',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Напишите дополнительные пожелания, комментарий (до 500 символов):',
                'failure_text': 'Такой город нам не известен',
                'handler': 'handle_comment',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Подтверждаете ли Вы правильность введенных данных? ( ДА / НЕТ):',
                'failure_text': 'Ответ непонятен, ответьте Да или Нет ',
                'handler': 'handle_confirm',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Ведите телефон для связи:',
                'failure_text': 'Некорректный телефонный номер, попробуйте снова',
                'handler': 'handle_phone',
                'next_step': 'last_step'
            },

            'last_step': {
                'text': 'Ваш заказ принят, с вами свяжутся по номеру {phone}\n\n',
                'failure_text': 'Билет не заказан. \n\n',
                'handler': None,
                'next_step': None
            }
        }
    }
}
