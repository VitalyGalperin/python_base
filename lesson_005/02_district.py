# -*- coding: utf-8 -*-
from district.central_street.house1.room1 import folks as folks1
from district.central_street.house1.room2 import folks as folks2
from district.central_street.house2.room1 import folks as folks3
from district.central_street.house2.room2 import folks as folks4
from district.soviet_street.house1.room1 import folks as folks5
from district.soviet_street.house1.room2 import folks as folks6
from district.soviet_street.house2.room1 import folks as folks7
from district.soviet_street.house2.room2 import folks as folks8

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join

print('На районе живут:', ', '.join(folks1), ',', ', '.join(folks2), ',', ', '.join(folks3), ',', ', '.join(folks4),
      ',', ', '.join(folks5), ',', ', '.join(folks6), ',', ', '.join(folks7), ',', ', '.join(folks8))
