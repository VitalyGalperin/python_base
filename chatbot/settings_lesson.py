GROUP_ID = 194114072
TOKEN = ''

INTENTS = [
    {
        'name': 'Дата',
        'tokens': ('когда', 'сколько', 'дата', 'даты', 'числ'),
        'scenario': None,
        'answer': 'Дата - ответ'
    },
    {
        'name': 'Место',
        'tokens': ('где', 'место', 'адрес'),
        'scenario': None,
        'answer': 'Где - ответ'
    },
    {
        'name': 'Регистрация',
        'tokens': ('регистр', 'добав', 'купи'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Ведите город отправления:',
                'failure_text': 'Такой город нам не известен',
                'handler': 'handle_departure',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Ведите город прибытия:',
                'failure_text': 'Такой город нам не известен',
                'handler': 'handle_arrival',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'На какую дату Вы хотите заказать билет?:',
                'failure_text': 'На эту дату, к сожалению, нет рейсов',
                'handler': 'handle_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Выберите номер рейса:',
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
                'text': 'Напишите дополнительные пожелания, комментарий:',
                'failure_text': 'Такой город нам не известен',
                'handler': 'handle_comment',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Подтверждаете ли Вы правильность введенных данных? ( ДА / НЕТ):',
                'failure_text': ' ',
                'handler': 'handle_confirm',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Ведите телефон для связи:',
                'failure_text': 'Некорректный номер, попробуйте снова',
                'handler': 'handle_phone',
                'next_step': 'step9'
            },

            'step9': {
                'text': 'Ваш заказ принят, с вами свяжутся по номеру {phone}',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}

DEFAULT_ANSWER = 'Не знаю как ответить'

DEFAULT_ANSWER = 'Не знаю как ответить'