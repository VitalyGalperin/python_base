# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


class AgeValueError(Exception):
    pass


with open('registrations.txt', 'r', encoding='utf8') as source, \
        open('registrations_good.log', 'w', encoding='utf8') as good_log, \
        open('registrations_bad.log', 'w', encoding='utf8') as bad_log:
    for line in source:
        try:
            original_line = line
            name, email, age = line.split(' ')
            if not name.isalpha():
                raise NotNameError()
            if email.find('@') == -1 or email.find('.') == -1:
                raise NotEmailError()
            if not 10 <= int(age) <= 99:
                raise AgeValueError()
            good_log.write(f'{original_line}')
        except ValueError as exc:
            bad_log.write(f'{original_line[:-1]:40} НЕ присутсвуют все три поля\n')
        except NotNameError as exc:
            bad_log.write(f'{original_line[:-1]:40} поле имени содержит НЕ только буквы\n')
        except NotEmailError as exc:
            bad_log.write(f'{original_line[:-1]:40} поле емейл НЕ содержит @ и .(точку)\n')
        except AgeValueError as exc:
            bad_log.write(f'{original_line[:-1]:40} поле возраст НЕ является числом от 10 до 99\n')
