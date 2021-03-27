#!/usr/local/bin/python
# -*- coding: utf-8 -*-from __future__ import print_function
import telebot 
bot = telebot.TeleBot('1787342730:AAExN5atfaxviT10ASvWhTIeHMiRFKhZxHE') #Токен бота
from telebot import types # Импорт модуля для работы кнопок
from datetime import datetime
import calendar
import locale 
from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import time, traceback
import threading
import logging
# #
# logging.basicConfig(filename='telebot.log',
#                     format = '%(asctime)s - [%(levelname)s] - %(message)s',
#                     level=logging.DEBUG,
#                     encoding='utf-8')#Создание лоигруещего файла, с уровнем логирования INFO(DEBUG записываться не будет)
#                                                                                  #кодинг utf-8
# logging.info('Bot is on. Start logging')#Запись в логирующий фалй о том что бот запущен
# #
CREDENTIALS_FILE = 'pytgbot-306409-16c86e02a8f5.json'  # Имя скаченного файла с закрытым ключом
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
spreadsheetId = '1GHGtG16XPKFo09bDrTVBFEL1A27VdQ9-m6l8gF8JtvQ' #ID Таблицы
#
date = datetime.isoweekday(datetime.now(tz=None))
days=['Понедельник', 'Вторник','Среда','Четверг','Пятница','Суббота']
#
# 
def print_date(ranges):
    """
    Функция получает "координаты" таблицы и создает расписание на день, в зависимости от введенынх координат.
    """          
    results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                         ranges = ranges, 
                                         valueRenderOption = 'FORMATTED_VALUE',  
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute() 
    sheet_values = results['valueRanges'][0]['values']
    s=str()
    k=int()
    if sheet_values[-1][0] in days:
        # Если последний и единственный элемент строки это день недели, то пар в этот день нет.
        return(f'{sheet_values[-1][0]}\nСегодня пар нет!')# Возвращает строку с днём недели и сообщение что пар нет
    else:
        for sheet in sheet_values:
            if sheet == []:
                #Если строка пустая (пары нет)
                k += 1 
                #Счётчик пар
                s = s + str(k) + ' пары нет! ' + '\n'# В переменную записывается номер пары и что она отсутствует
            else:
                #Если пара есть
                if str(sheet[0]) in days:
                    # Если строка это название дня недели счётчик пар не срабатывает
                    # и в переменную просто добавляется этот день с переносом на следующую строку
                    s = s + str(sheet[0]) + '\n'
                else:
                    # Если пара есть и она не название дня недели
                    k += 1# Счётчик пар
                    if sheet == sheet_values[-1]:
                        # Если пара последняя то записывается номер пары и пара без переноса строки
                        s = s + str(k) + ' пара: ' + str(sheet[0])
                    else:
                        # Если пара не последня то записывается номер пары и пара с переносом строки
                        s = s + str(k) + ' пара: ' + str(sheet[0]) + '\n'
        return(s)# Возвращает полученную строку
#
def tomorrow(rasp, date):
    """
    Функция получает координаты таблицы, где rasp - это название группы, а date номер дня недели.
    """
    if date == 1:
        return(f"{rasp}C2:C7")
    elif date == 2:
        return(f"{rasp}D2:D7")
    elif date == 3:
        return(f"{rasp}E2:E7")
    elif date == 4:
        return(f"{rasp}F2:F7")
    elif date == 5:
        return(f"{rasp}G2:G7")
    elif date == 7:
        return(f"{rasp}B2:B7")
#
# Расписание звонков. \n переводит на следующую строчку
pnpt = u"1 пара: 8:30 — 10:05\n2 пара: 10:15 — 11:50\nОбед: 11:50 — 12:35\n3 пара: 12:35 — 14:10\n4 пара: 14:20 — 15:55\n5 пара: 16:05 — 17:40\n6 пара: 17:50 — 19:25"
subb = u"1 пара: 8:30 — 10:05\n2 пара: 10:15 — 11:50\n3 пара: 12:00 — 13:40\n4 пара: 13:50 — 15:25\n5 пара: 15:35 — 17:10\n6 пара: 17:20 — 18:55"
predpr = u"1 пара: 8:30 — 10:05\n2 пара: 10:15 — 11:50\n3 пара: 12:00 — 13:40\n4 пара: 13:50 — 14:50\n5 пара: 15:00 — 16:00"
#
#
def auto_update():
    """
    Функция auto_update отвечает за обновление данных полученных из таблицы.
    """

    ranges=['B2:B7','C2:C7','D2:D7','E2:E7','F2:F7','G2:G7']# Координаты для таблицы
    g1 = 'Расписание гр.081!'
    g2 = 'Расписание гр.082!'
    date = datetime.isoweekday(datetime.now(tz=None))# Получение номера дня недели

    logging.info('START CREATING SCHEDULES')
    global group1_today, group1_tomorrow, group1_week, group2_today, group2_tomorrow, group2_week
    # Объявление глобальных переменных
    if not date == 6:
        # Если сегодня не суббота
        group1_tomorrow = print_date(tomorrow(g1,date))# Создание расписания на завтра для группы 081
        group2_tomorrow = print_date(tomorrow(g2,date))# Создание расписания на завтра для группы 082
    logging.info('TOMORROW CREATED')
    if not date == 7:
        # Если сегодня не воскресенье
        g1_td = g1 + ranges[date-1]
        group1_today=print_date(g1_td)# Создание расписания на сегодня для группы 081. [date-1] т.к. в списке date "Понедельник" - это 0 элемент
        g2_td = g2 + ranges[date-1]
        group2_today = print_date(g2_td)# Создание расписания на сегодня для группы 082. [date-1] т.к. в списке date "Понедельник" - это 0 элемент
    else:
        # Если сегодня воскресенье
        group1_today='Сегодня воскресенье чел... Пар нет'
        group2_today='Сегодня воскресенье чел... Пар нет'
    logging.info('TODAY CREATED')
    gr1_week = str()
    for i in range(0,6):
        # Создание расписания на неделю для 081
        gr = g1 + ranges[i]# Генерация координат таблицы с 0 дня - Понедельника, по 6 - Субботу
        gr1_week = gr1_week + '\n' + print_date(gr) + '\n'# Запись расписаний в переменную
    group1_week = gr1_week# Дополнительная переменная для того, что бы во время обновления данных, не выводилось не полное расписание на неделю
    gr2_week = str()
    for i in range(0,6):
        # Создание расписания на неделю для 082
        gr = g2 + ranges[i]# Генерация координат таблицы с 0 дня - Понедельника, по 6 - Субботу
        gr2_week = gr2_week + '\n' + print_date(gr) + '\n'# Запись расписаний в переменную
    group2_week = gr2_week# Дополнительная переменная для того, что бы во время обновления данных, не выводилось не полное расписание на неделю
    logging.info('WEEK CREATED')
    logging.info('FINISHED CREATING SCHEDULES FOR GROUPS')
#
@bot.message_handler(commands=['start'])# Реагирует на /start
def start_message(message):
    logging.info(f'chat_id = {message.chat.id}|username = {message.chat.username}|message = {message.text}')# Запись в логирующий файл с ID чата, никнеймом и сообщением
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('081', '082')# Создание кнопок "081" и "082"
    keyboard.row('Расписание звонков')# Создание кнопки "Расписание звонков" на новой строчке
    keyboard.row('Методичка')# Создание кнопки "Методичка" на новой строчке
    bot.send_message(message.chat.id, 'Привет, выбери нужное. Если что, пользоваться нужно кнопками снизу.', reply_markup=keyboard)# Ответ бота и вывод клнопок под чатом
#   
@bot.message_handler(commands=['report'])# Реагирует на /report
def start_message(message):
    logging.info(f'chat_id = {message.chat.id}|username = {message.chat.username}|message = {message.text}')# Запись в логирующий файл с ID чата, никнеймом и сообщением
    if message.text == '/report':
        # Если сообщение содержит только /report предлагается ввести сообщение с командой /report
        bot.send_message(message.chat.id, 'Введите ваше предложение или сообщение об ошибке с командой /report')
    else:
        # Пересылает сообщение пользователя в лс администратору с информацией о том кто отправил репорт(никнейм и айди чата)
        bot.send_message(882503361, f'"{message.text}" report from {message.chat.username}[{message.chat.id}]')
#
@bot.message_handler(content_types=['text'])# Метод, который получает сообщения и обрабатывает их
def get_text_messages(message):
    logging.info(f'chat_id = {message.chat.id}|username = {message.chat.username}|message = {message.text}')
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    if message.text == "081": 
        # Выполняется, если выбрали 081 гр.
        keyboard.row('Расписание на сегодня (гр. 081)')
        keyboard.row ('Расписание на завтра (гр. 081)')
        keyboard.row ('Расписание на неделю (гр. 081)')
        keyboard.row ('Главное меню')
        # Выводит на экран клавиатуру с кнопками
        bot.send_message(message.chat.id, "Выбрана группа 081.", reply_markup=keyboard)
        # Бот отправляет сообщение пользователю о том что выбрана группа 081 и показывает клавиатуру на экране
    elif message.text == "082": 
        # Выполняется, если выбрали 082 гр.
        keyboard.row('Расписание на сегодня (гр. 082)')
        keyboard.row('Расписание на завтра (гр. 082)')
        keyboard.row('Расписание на неделю (гр. 082)')
        keyboard.row('Главное меню') 
        # Выводит на экран клавиатуру с кнопками
        bot.send_message(message.chat.id, "Выбрана группа 082.", reply_markup=keyboard)
        # Бот отправляет сообщение пользователю о том что выбрана группа 082 и показывает клавиатуру на экране
    elif message.text == "Главное меню":
        keyboard.row('081', '082')
        keyboard.row('Расписание звонков')
        keyboard.row('Методичка')
        bot.send_message(message.chat.id, 'Ты вернулся в главное меню. Выбери нужное.', reply_markup=keyboard)
    elif message.text == "Расписание на сегодня (гр. 081)":
         bot.send_message(message.chat.id, group1_today)
    elif message.text == "Методичка":
        text = '[Yandex Диск](https://yadi.sk/d/mBwwk_1QULpXaw)'
        bot.send_message(message.chat.id, text, parse_mode='MarkdownV2', reply_markup=keyboard)
    elif message.text == "Расписание звонков":
        keyboard.row('День сурка (Пн-ПТ)')
        keyboard.row('Суббота')
        keyboard.row('Предпраздничные дни')
        keyboard.row('Главное меню') 
        bot.send_message(message.chat.id, 'Что интересует?', reply_markup=keyboard)
    elif message.text == "День сурка (Пн-ПТ)":
        bot.send_message(message.chat.id, pnpt, reply_markup=keyboard)
    elif message.text == "Суббота":
        bot.send_message(message.chat.id, subb, reply_markup=keyboard)
    elif message.text == "Предпраздничные дни":
        bot.send_message(message.chat.id, predpr, reply_markup=keyboard)
    elif message.text == "Расписание на сегодня (гр. 082)":
         bot.send_message(message.chat.id, group2_today)
    elif message.text == "Расписание на завтра (гр. 081)":
        date = datetime.isoweekday(datetime.now(tz=None))
        if date == 6:
            bot.send_message(message.chat.id, 'Завтра пар нет. Отдыхаем!')
        else:
            bot.send_message(message.chat.id, group1_tomorrow)
    elif message.text == "Расписание на завтра (гр. 082)":
        date = datetime.isoweekday(datetime.now(tz=None))
        if date == 6:
            bot.send_message(message.chat.id, 'Завтра пар нет. Отдыхаем!')
        else:
            bot.send_message(message.chat.id, group2_tomorrow)
    elif message.text == "Расписание на неделю (гр. 081)":
        bot.send_message(message.chat.id, group1_week)
    elif message.text == "Расписание на неделю (гр. 082)":
        bot.send_message(message.chat.id, group2_week)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Воспользуйся кнопками на экране.")
#
auto_update()# Вызов функции с обновлением данных расписаний
#
def every(delay, task):
    """
    Функция вызывающая функцию с задержкой в секундах
    """
    next_time = time.time() + delay# В переменную записывается время, через которое должна сработать функция. time.time() - время в настоящий момент, delay - задержка
    while True:
        # Бесконечный цикл
        time.sleep(max(0, next_time - time.time()))# max возвращает большее из чисел. Пока next_time больше time.time(время прямо сейчас)
        try:
            task()
        except Exception:
            traceback.print_exc()
        next_time += (time.time() - next_time) // delay * delay + delay
#
threading.Thread(target=lambda: every(3600, auto_update)).start()# Запускает вызов функции every в многопоточном режиме, что не мешает работе основной программы
#
if __name__ == '__main__':
    bot.infinity_polling()# Бесконечная проверка чата с ботом на сообщения.