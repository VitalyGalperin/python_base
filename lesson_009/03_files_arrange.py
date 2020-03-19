# -*- coding: utf-8 -*-

import os, time, shutil

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится ктолько к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


import os
import time
from shutil import copy2, copyfileobj
import zipfile


class FileOrder:

    def __init__(self, source_path=False, recipient_path=False, source_file=''):
        self.source_file = source_file
        self.image_extension = ['.png', '.jpg', '.bmp', '.mp4', '.mov']
        if not source_path:
            self.source_path = os.path.normpath(os.path.abspath(os.curdir))
        if not recipient_path:
            self.recipient_path = os.path.normpath(os.path.abspath(os.curdir))

    def directory_sort(self):
        for dirpath, dirnames, filenames in os.walk(self.source_path):
            for file_name in filenames:
                name, extension = os.path.splitext(file_name)
                if extension in self.image_extension:
                    source_full_path = os.path.join(dirpath, file_name)
                    struct_file_date = time.gmtime(os.path.getmtime(source_full_path))
                    struct_path = 'icons_by_year/' + str(struct_file_date.tm_year) + '/' + str(
                        struct_file_date.tm_mon) + '/'
                    if not os.path.isdir(struct_path):
                        os.makedirs(struct_path)
                    recipient_full_path = struct_path + file_name
                    if not os.path.isfile(recipient_full_path):
                        copy2(source_full_path, recipient_full_path)

    def archive_sort(self):
        source_zip = zipfile.ZipFile(self.source_file)
        #copy_zip = source_zip.open(source_zip)
        for file_name in source_zip.infolist():
            name, extension = os.path.splitext(file_name.filename)
            file_name.filename = os.path.split(name)[1]
            print(file_name.filename)
            only_name = os.path.split(name)[1]
            if extension in self.image_extension:
                struct_path = 'icons_by_year/' + str(file_name.date_time[0]) + '/' + str(
                    file_name.date_time[1]) + '/'
                file_name.filename = os.path.basename(file_name.filename)
                if not os.path.isdir(struct_path):
                    os.makedirs(struct_path)
                if not os.path.isfile(struct_path + only_name):
                    print(file_name.filename)
                    # copyfileobj(file_name.filename, struct_path)
                    source_zip.extract(file_name.filename, struct_path)




# sort_dir = FileOrder()
# sort_dir.directory_sort()

# Для проверки работы с ZIP-файлом надо удалить директории /icons и /icons_by_year
# и закомментировать две предыдущие строки кода

sort_zip = FileOrder(source_file='icons.zip')
sort_zip.archive_sort()
