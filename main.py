import telebot
from telebot import types
from aiogram.utils.markdown import hlink

file = open("TOKEN.txt", "r")
token = file.readline()
file.close()
bot = telebot.TeleBot(token)

hello_url = hlink("Привет, я твой личный помошник", "https://youtu.be/dQw4w9WgXcQ")

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
    bot.send_message(message.chat.id, f"{hello_url}. Начинаем работу.\nВведите команду:",parse_mode='HTML')
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['info'])
def info(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = "Страница новичка"
    btn2 = "Документы"
    btn3 = "Отпуск/Больничный/Отгул"
    btn4 = "Бенефит"
    btn5 = "Службы"
    btn6 = "FAQ"
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
        btn4 = "Бенефит"
        btn5 = "Службы"
        btn6 = "FAQ"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=reply_markup)
    if message.text == "Документы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Шаблоны"
        btn2 = "Справки"
        btn3 = "Расчетный лист"
        btn4 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите нужный документ:", reply_markup=reply_markup)
    if message.text == "Отпуск/Больничный/Отгул":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Отпуск"
        btn2 = "Больничный"
        btn3 = "Отгул"
        btn4 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите:", reply_markup=reply_markup)
    if message.text == "Страница новичка":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Для разработчика"
        btn2 = "Для аналиткика"
        btn3 = "Страничка новичка БАРС Груп"
        btn4 = "Вернуться в главное меню"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите:", reply_markup=reply_markup)


bot.polling(non_stop=True)
