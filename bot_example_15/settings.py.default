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
                'text': 'Имя',
                'failure_text': 'не то имя',
                'handler': 'handle_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'email',
                'failure_text': 'not email',
                'handler': 'handle_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': '{name}  {email}',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },

        }
    }
}

DEFAULT_ANSWER = 'Не знаю как ответить'
