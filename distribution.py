import sqlite3
import telebot
import os
from dotenv.main import load_dotenv

userWithRoots = [502643682]
load_dotenv()
token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)
conn = sqlite3.connect('newUsers.db', check_same_thread=False)
cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users(
#    userid INTEGER PRIMARY KEY autoincrement,
#    idtelegram TEXT,
#    startdate DATE);
#  """)
# conn.commit()


def insertsql(entity):
    cur.execute('INSERT INTO users(idtelegram,startdate) VALUES(?,?)', entity)


def selectsql7():
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 7 and julianday('now') - julianday(startdate) < 8")
    return cur.fetchall()

def selectsql30():
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 30 and julianday('now') - julianday(startdate) < 31")
    return cur.fetchall()


def selectsql92():
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 92 and julianday('now') - julianday(startdate) < 93")
    return cur.fetchall()


@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        user_id = message.chat.id

        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            entity = (user_items[1], user_items[2])
            insertsql(entity)
            conn.commit()
        else:
            bot.send_message(message.chat.id, "У вас нет прав")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка")


# @bot.message_handler(commands=['test'])
# def test(message):
#     list_of_users = selectsql()
#     for user in list_of_users:
#         bot.send_message(user[0], "Hello")


def check_dates():
    list_of_users7 = selectsql7()
    for user in list_of_users7:
        bot.send_message(user[0], "Hello my niggas")
    list_of_users30 = selectsql30()
    for user in list_of_users30:
        bot.send_message(user[0], "Hello my niggas")
    list_of_users92 = selectsql92()
    for user in list_of_users92:
        bot.send_message(user[0], "Hello my niggas")


check_dates()

bot.polling(non_stop=True)
