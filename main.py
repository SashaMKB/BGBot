import telebot
from telebot import types
from links import *

file = open("TOKEN.txt", "r")
token = file.readline()
file.close()
bot = telebot.TeleBot(token)

todos = dict()

HELP = '''
Список доступных команд:
/info - список доступных команд
/show  - напечать все задачи на заданную дату
/todo - добавить задачу
/help - Напечатать help
'''


@bot.message_handler(commands=['start'])
def start(message):
    # bot.send_message(message.chat.id, f"{hello_url}. Начинаем работу.\nВведите команду:", parse_mode='HTML')
    bot.send_message(message.chat.id, "Привет-привет!\nМеня зовут ...\nРад приветствовать тебя.\nЯ помогу тебе найти "
                                      "ответы на твои вопросы.\nЧто тебя интересует?")
    # bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['info'])
def info(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = "Страница новичка"
    btn2 = "Документы"
    btn3 = "Отпуск/Больничный/Отгул"
    btn4 = "Плюшки"
    btn5 = "Службы"
    btn6 = "Идеи"
    reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Выберите интересующий вопрос:", reply_markup=reply_markup)


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['todo'])
def add(message):
    try:
        _, date, tail = message.text.split(maxsplit=2)
        task = ' '.join([tail])
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату: {date}')
    except Exception:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ещё раз")


@bot.message_handler(commands=['show'])
def print_(message):
    try:
        i = 1
        date = message.text.split()[1].lower()
        if date in todos:
            tasks = ''
            for task in todos[date]:
                tasks += f'[{i}] {task}\n'
                i += 1
        else:
            tasks = 'Такой даты нет'
        bot.send_message(message.chat.id, tasks)
    except Exception:
        print(Exception)
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова")


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Вернуться в главное меню":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Страница новичка"
        btn2 = "Документы"
        btn3 = "Отпуск/Больничный/Отгул"
        btn4 = "Плюшки"
        btn5 = "Службы"
        btn6 = "Идеи"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, text="Unknown", reply_markup=reply_markup)
    if message.text == "Документы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Шаблоны"
        btn2 = "Справки"
        btn3 = "Расчетный лист"
        btn4 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4)
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
        btn1 = "Отпуск"
        btn2 = "Больничный"
        btn3 = "Отгул"
        btn4 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Оформи отпуск/больничный/отгул правильно, чтоб тебя не беспокоили в эти дни",
                         reply_markup=reply_markup)
    if message.text == "Отпуск":
        bot.send_message(message.chat.id, f"{vacation_url}", parse_mode='HTML')
    if message.text == "Больничный":
        bot.send_message(message.chat.id, f"{sickleave_url}", parse_mode='HTML')
    if message.text == "Отгул":
        bot.send_message(message.chat.id, f"Пока что тут пусто...")

    if message.text == "Страница новичка":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Для разработчика"
        btn2 = "Для аналитика"
        btn3 = "Страничка новичка БАРС Груп"
        btn4 = "Страничка новичка БЦ ЖКХ,СЗ и СТРК"
        btn5 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id,
                         "Здесь собрана вся информация, которая будет полезна для новичка.\nЕсли останутся вопросы, можешь обратиться к наставнику/рукводителю/HR",
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
        btn5 = "Вернуться в главное меню"
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
        btn5 = "Пропуск"
        btn6 = "Канцтовары, Чай"
        btn7 = "Вернуться в главное меню"
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
    if message.text == "Пропуск":
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


bot.polling(non_stop=True)
