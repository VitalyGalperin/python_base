# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.

class Water:

    def __str__(self):
        return 'Вода'

    def __add__(self, other):
        if isinstance(other, Air):
            return Storm(water=self, air=other)
        if isinstance(other, Fire):
            return Steam(water=self, fire=other)
        if isinstance(other, Earth):
            return Creek(water=self, earth=other)

    def __pow__(self, other=2):
        return Ocean()


class Air:

    def __str__(self):
        return 'Воздух'

    def __add__(self, other):
        if isinstance(other, Water):
            return Storm(air=self, water=other)
        if isinstance(other, Fire):
            return SkyLightning(air=self, fire=other)
        if isinstance(other, Earth):
            return Dust(air=self, earth=other)

    def __pow__(self, other=2):
        return Tornado()


class Fire:

    def __str__(self):
        return 'Огонь'

    def __add__(self, other):
        if isinstance(other, Water):
            return Steam(fire=self, water=other)
        if isinstance(other, Air):
            return FireLightning(fire=self, air=other)
        if isinstance(other, Earth):
            return Lava(fire=self, earth=other)

    def __pow__(self, other=2):
        return Plasma()


class Earth:

    def __str__(self):
        return 'Земля'

    def __add__(self, other):
        if isinstance(other, Water):
            return Dirt(earth=self, water=other)
        if isinstance(other, Air):
            return Dust(earth=self, air=other)
        if isinstance(other, Fire):
            return Lava(earth=self, fire=other)

    def __pow__(self, other=2):
        return Diamond()


class Storm:

    def __init__(self, air, water):
        self.air = air
        self.water = water

    def __str__(self):
        return 'Шторм'


class SkyLightning:

    def __init__(self, air, fire):
        self.air = air
        self.fire = fire

    def __str__(self):
        return 'Небесная Молния'

    def __add__(self, other):
        if isinstance(other, Steam):
            return LuminousCloud(sky_lightning=self, steam=other)


class FireLightning:

    def __init__(self, fire, air):
        self.air = air
        self.fire = fire

    def __str__(self):
        return 'Огненная Молния'


class Dust:

    def __init__(self, air, earth):
        self.air = air
        self.earth = earth

    def __str__(self):
        return 'Пыль'


class Steam:

    def __init__(self, water, fire):
        self.water = water
        self.fire = fire

    def __str__(self):
        return 'Пар'

    def __add__(self, other):
        if isinstance(other, SkyLightning):
            return Vipe(steam=self, sky_lightning=other)


class Lava:

    def __init__(self, earth, fire):
        self.earth = earth
        self.fire = fire

    def __str__(self):
        return 'Лава'


class Dirt:

    def __init__(self, water, earth):
        self.earth = earth
        self.water = water

    def __str__(self):
        return 'Грязь'


class Creek:

    def __init__(self, earth, water):
        self.earth = earth
        self.water = water

    def __str__(self):
        return 'Ручей'


class LuminousCloud:

    def __init__(self, sky_lightning, steam):
        self.sky_lightning = sky_lightning
        self.steam = steam

    def __str__(self):
        return 'Светящееся облако'


class Vipe:

    def __init__(self, steam, sky_lightning):
        self.sky_lightning = sky_lightning
        self.steam = steam

    def __str__(self):
        return 'Vipe'


class Diamond:

    def __str__(self):
        return 'Бриллиант'


class Ocean:

    def __str__(self):
        return 'Океан'


class Tornado:

    def __str__(self):
        return 'Смерч'

    def __add__(self, other):
        if isinstance(other, Plasma):
            return BlackHole(tornado=self, plasma=other)


class Plasma:

    def __str__(self):
        return 'Плазма'

    def __add__(self, other):
        if isinstance(other, Tornado):
            return BlackHole(plasma=self, tornado=other)


class BlackHole:

    def __init__(self, tornado, plasma):
        self.plasma = plasma
        self.tornado = tornado

    def __str__(self):
        return 'Черная Дыра'


print(Water(), '+', Air(), '=', Water() + Air())
print(Air(), '+', Water(), '=', Air() + Water())
print('-----------------------------------------------------------------')
print(Fire(), '+', Air(), '=', Fire() + Air())
print(Air(), '+', Fire(), '=', Air() + Fire())
print('-----------------------------------------------------------------')
print(Fire(), '+', Water(), '=', Fire() + Water())
print(Water(), '+', Fire(), '=', Water() + Fire())
print('-----------------------------------------------------------------')
print(Fire(), '+', Earth(), '=', Fire() + Earth())
print(Earth(), '+', Fire(), '=', Earth() + Fire())
print('-----------------------------------------------------------------')
print(Earth(), '+', Water(), '=', Earth() + Water())
print(Water(), '+', Earth(), '=', Water() + Earth())
print('-----------------------------------------------------------------')
print(Water(), '+', Air(), '=', Water() + Air())
print(Air(), '+', Water(), '=', Air() + Water())
print('-----------------------------------------------------------------')
print(Earth(), '+', Air(), '=', Earth() + Air())
print(Air(), '+', Earth(), '=', Air() + Earth())
print('-----------------------------------------------------------------')
print(SkyLightning(Air(), Water()), '+', Steam(Water(), Fire()), '=',
      (SkyLightning(Air(), Water()) + Steam(Water(), Fire())))
print(Steam(Water(), Fire()), '+', (SkyLightning(Air(), Water())), '=',
      Steam(Water(), Fire()) + (SkyLightning(Air(), Water())))
print('-----------------------------------------------------------------')
print(Earth(), '** 2 =', Earth() ** 2)
print('-----------------------------------------------------------------')
print(Air(), '** 2 =', Air() ** 2)
print('-----------------------------------------------------------------')
print(Fire(), '** 2 =', Fire() ** 2)
print('-----------------------------------------------------------------')
print(Water(), '** 2 =', Water() ** 2)
print('-----------------------------------------------------------------')
print(Air() ** 2, '+', Fire() ** 2, '=', Air() ** 2 + Fire() ** 2)
print(Fire() ** 2, '+', Air() ** 2, '=', Fire() ** 2 + Air() ** 2)
print('-----------------------------------------------------------------')

# Зачет
