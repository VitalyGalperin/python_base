from pony.orm import Database, Required, Json
from bot_example_16.settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """Состояние пользователя внутри сценария"""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """Заявка на регистрацию"""
    name = Required(str)
    email = Required(str)


db.generate_mapping(create_tables=True)


DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='q',
    host='localhost',
    database='vk_chat_bot'
)