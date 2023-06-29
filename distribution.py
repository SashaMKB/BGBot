import sqlite3
import telebot
import os
from dotenv.main import load_dotenv
from sqlrequests import *

userWithRoots = []
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
   startdate DATE);
 """)
conn.commit()


@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        user_id = message.chat.id

        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5])
            insertsql(entity, cur)
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


def check_dates():
    list_of_users7 = selectsql7(cur)
    for user in list_of_users7:
        bot.send_message(user[0], "Hello my friends")
    list_of_users30 = selectsql30(cur)
    for user in list_of_users30:
        bot.send_message(user[0], "Hello my niggas")
    list_of_users92 = selectsql92(cur)
    for user in list_of_users92:
        bot.send_message(user[0], "Hello my niggas")


bot.polling(non_stop=True)
