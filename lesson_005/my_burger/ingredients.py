# -*- coding: utf-8 -*-

def add_bun():
    print('За основу возьмем булочку. разрезаем её пополам вдоль и слегка поджаривем на гриле место разреза')
    print('Разрезаем её пополам вдоль и слегка поджаривем на гриле место разреза')
    print('Используем нижнюю часть булочки как основу')

def add_cutlet():
    print('Берём котлету, обжариваем на гриле с двух сторон')
    add_layr_to_burger()

def add_chees():
    print('Достаём из упаковки порционный кусочек сыра')
    add_layr_to_burger()

def add_cucumber():
    print('Берём 3 порционных кусочка огурца')
    add_layr_to_burger()

def add_tomato():
    print('Берём 2 нарезанные кусочка помидора')
    add_layr_to_burger()

def add_onion():
    print('Берём 2 нарезанные кусочка лука')
    add_layr_to_burger()

def add_mayonnaise():
    print('Берём порцию майонеза')
    smear_up()

def add_sauce():
    print('ББерём порцию соуса')
    smear_up()

def add_mustard():
    print('Берём порцию горчицы')
    smear_up()

def add_cover():
    print('Накрываем сверху второй половиной булочки')

def service():
    print('Заворачиваем бургер в упаковку')
    print('Бургер готов к употреблению')

def add_layr_to_burger():
    print('Довавляем в бургер следующим слоем')

def smear_up():
    print('Намазываем сверху')