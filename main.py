import schedule
from telebot import types
from links import *
import sqlite3
import telebot
import os
from sqlrequests import *
from dotenv.main import load_dotenv
import time
import threading

userWithRoots = [502643682]

load_dotenv()
token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)
conn = sqlite3.connect('newUsers.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY autoincrement,
   surname TEXT,
   name TEXT,
   secondname TEXT,
   idtelegram TEXT,
   startdate DATE,
   mentor TEXT DEFAULT 'nobody');
 """)
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = "Страница новичка🧑‍💻"
    btn2 = "Документы"
    btn3 = "Отпуск/Больничный/Отгул"
    btn4 = "Плюшки"
    btn5 = "Службы"
    btn6 = "Идеи"
    reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id,
                     "Привет-привет!\nМеня зовут Джулиус\nРад приветствовать тебя.\nЯ помогу тебе найти "
                     "ответы на твои вопросы.\nЧто тебя интересует?", reply_markup=reply_markup)


@bot.message_handler(commands=['instruction'])
def instruction(message):
    bot.send_message(message.chat.id, '''
    1)Для добавления стажера введите команду "/add (Фамилия) (Имя) (Отчество) (ID Telegram) (Дата первого рабочего дня) (Юзернейм ментора)".
Обратите внимание, что дату нужно вводить в формате(ГГГГ-ММ-ДД).В случае некорректного ввода, может неправильно присылаться рассылка(или вообще не присылаться)
Добавляйте стажера только после его регистрации в боте!

2) Для просмотра всех стажёров введите "/show"

3) Для удаления стажера из списка стажеров введите команду "/delete (ID Telegram)"
''')


@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            if len(user_items) == 7:
                entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5], user_items[6])
                insertsql1(entity, cur)
            else:
                entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5])
                insertsql2(entity, cur)
            conn.commit()
        else:
            bot.send_message(message.chat.id, "У вас нет прав")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка")


@bot.message_handler(commands=["show"])
def show(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            show_sql(bot, user_id, cur)
        else:
            bot.send_message(user_id, "У вас нет прав")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка")


@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            print(user_items[1])
            delete_user(user_items[1], cur)
            conn.commit()
        else:
            bot.send_message(user_id, "У вас нет прав")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка")


# @bot.message_handler(commands=['update'])
# def update(message):
#     try:
#         user_id = message.chat.id
#         if user_id in userWithRoots:
#             user_items = message.text.split(" ")
#             print(user_items)
#             entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5])
#             updatesql(entity, cur)
#             conn.commit()
#         else:
#             bot.send_message(message.chat.id, "У вас нет прав")
#     except Exception:
#         bot.send_message(message.chat.id, "Ошибка")


def check_dates():
    list_of_users7 = selectsql7(cur)
    if len(list_of_users7) != 0:
        for user in list_of_users7:
            bot.send_message(user[0], "Hello my friends")
    list_of_users30 = selectsql30(cur)
    if len(list_of_users30) != 0:
        for user in list_of_users30:
            bot.send_message(user[0], "Hello my niggas")
    list_of_users92 = selectsql92(cur)
    if len(list_of_users92) != 0:
        for user in list_of_users92:
            bot.send_message(user[0], "Hello my niggas")


schedule.every().day.at("10:30").do(check_dates)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Вернуться в главное меню ↩":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Страница новичка🧑‍💻"
        btn2 = "Документы"
        btn3 = "Отпуск/Больничный/Отгул"
        btn4 = "Плюшки"
        btn5 = "Службы"
        btn6 = "Идеи"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, text="Что Вы хотите узнать?", reply_markup=reply_markup)
    if message.text == "Документы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Шаблоны"
        btn3 = "Расчетный лист"
        btn4 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn3, btn4)
        bot.send_message(message.chat.id, "Здесь собраны самые актуальные документы, которые тебе могут понадобиться",
                         reply_markup=reply_markup)
    if message.text == "Расчетный лист":
        bot.send_message(message.chat.id, '''
        "Получение расчетного листа доступно через telegram-бота БАРС Груп:

1️⃣ Перейти на @barsofficebot 
2️⃣ Написать команду /start 
3️⃣ Выбрать команду /paysheet в приветственном сообщении 
4️⃣ Указать период в формате номер месяца_год .

❗️ВАЖНО: к выгрузке доступны только предыдущие периоды. 

Стоит учитывать: за только что прошедший месяц расчетный лист появляется не раньше 7го числа. Например, если 1го сентября запросить данные за август, то расчетный лист не сформируется. Доступ к нему откроется после 7го сентября. 

5️⃣ Дать своё согласие на получение данных (единоразово) 
6️⃣ Дождаться выгрузки файлов формата pdf 


⚠️ Дополнительная информация:
1. Функционал недоступен уволившимся сотрудникам.
2. Если бот возвращает сообщение: ""Данные по сотруднику не найдены"", обратитесь в СТП.
3. В периоды пиковой нагрузки выгрузка листа может занять некоторое время, пока ваш запрос стоит в очереди на обработку, но он в любом случае будет выполнен."
        ''')
    if message.text == "Шаблоны":
        bot.send_message(message.chat.id, f"{templates_url}", parse_mode='HTML')
    if message.text == "Отпуск/Больничный/Отгул":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Отпуск 🏖"
        btn2 = "Больничный"
        btn3 = "Отгул"
        btn4 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Оформи отпуск/больничный/отгул правильно, чтоб тебя не беспокоили в эти дни",
                         reply_markup=reply_markup)
    if message.text == "Отпуск 🏖":
        bot.send_message(message.chat.id, f"{vacation_url}", parse_mode='HTML')
    if message.text == "Больничный":
        bot.send_message(message.chat.id, f"{sickleave_url}", parse_mode='HTML')
    if message.text == "Отгул":
        bot.send_message(message.chat.id, f"Пока что тут пусто...")

    if message.text == "Страница новичка🧑‍💻":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Для разработчика"
        btn2 = "Для аналитика"
        btn3 = "Страничка новичка БАРС Груп"
        btn4 = "Страничка новичка БЦ ЖКХ,СЗ и СТРК"
        btn5 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id,
                         "Здесь собрана вся информация, которая будет полезна для новичка.\nЕсли останутся вопросы, "
                         "можешь обратиться к наставнику/рукводителю/HR",
                         reply_markup=reply_markup)
    # нужно ли добавить страничку новичка БЦ ЖКХ --?
    if message.text == "Для разработчика":
        bot.send_message(message.chat.id, f"{dev_url}", parse_mode="HTML")
    if message.text == "Для аналитика":
        bot.send_message(message.chat.id, f"{an_url}", parse_mode='HTML')
    if message.text == "Страничка новичка БАРС Груп":
        bot.send_message(message.chat.id, f"{newpie_utl}", parse_mode='HTML')
    if message.text == "Страничка новичка БЦ ЖКХ,СЗ и СТРК":
        bot.send_message(message.chat.id, f'{newjkx_url}', parse_mode="HTML")

    if message.text == "Плюшки":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "ДМС"
        btn2 = "Реферальная программа"
        btn3 = "БАРС-КОД"
        btn4 = "Библиотека"
        btn5 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выберите:", reply_markup=reply_markup)
    if message.text == "ДМС":
        bot.send_message(message.chat.id, f"{dms_url}", parse_mode="HTML")
    if message.text == "Реферальная программа":
        bot.send_message(message.chat.id, f"{referalprogram_url}", parse_mode="HTML")
    if message.text == "БАРС-КОД":
        bot.send_message(message.chat.id, f"{code_url}", parse_mode="HTML")
    if message.text == "Библиотека":
        bot.send_message(message.chat.id, f"{biblio_url}", parse_mode="HTML")
    if message.text == "Службы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Бухгалтерия"
        btn2 = "Техподдержка"
        btn3 = "Кадры"
        btn4 = "Корпоративный университет"
        btn5 = "Пропуск 🪪"
        btn6 = "Канцтовары, Чай"
        btn7 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.send_message(message.chat.id, "В БАРС Груп много служб, которые помогают организовывать работу Компании:",
                         reply_markup=reply_markup)

    if message.text == "Бухгалтерия":
        bot.send_message(message.chat.id,
                         f"Тебе нужно заказать справку 2-НДФЛ или есть вопросы по начислению ЗП, тогда тебе в {accounting_url}",
                         parse_mode="HTML")
    if message.text == "Техподдержка":
        bot.send_message(message.chat.id, f"{techsupport_url}", parse_mode="HTML")
    if message.text == "Кадры":
        bot.send_message(message.chat.id,
                         f"Сколько дней отпуска? Нужен пакет документов для военкомата? Или справка с места работы? Со всеми этими вопросами поможет разобраться {personnel_url}",
                         parse_mode="HTML")
    if message.text == "Корпоративный университет":
        bot.send_message(message.chat.id,
                         f"Корпоративный университет помогает развивать Soft и Hard навыки наших сотрудников. Список обучений, курсов, бизнес игры  можно посмотреть {corporateUn_url}",
                         parse_mode="HTML")
    if message.text == "Пропуск 🪪":
        bot.send_message(message.chat.id,
                         f"Пропуск перестал работать или необходим пропуск на велопарковку?В этом случае необходимо поставить задачу {pass_url}",
                         parse_mode="HTML")
    if message.text == "Канцтовары, Чай":
        bot.send_message(message.chat.id,
                         "Чай и сахар можно взять у офис-менеджера на 5 этаже.За канцелярией иди к офис-менеджеру на 7 этаж (правый вход)",
                         parse_mode="HTML")
    if message.text == "Идеи":
        bot.send_message(message.chat.id,
                         f"Если у тебя  есть идеи, пиши {ideas_url}.Мы обязательно рассмотрим твою идею, а ты получишь классный мерч БЦ",
                         parse_mode="HTML")


def func1():
    bot.polling(non_stop=True)


def func2():
    while True:
        schedule.run_pending()
        time.sleep(1)


bot_thread = threading.Thread(target=func1)
while_tread = threading.Thread(target=func2)

bot_thread.start()
while_tread.start()
