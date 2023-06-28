import pandas
import sqlite3
import telebot
import telebot
import os
from dotenv.main import load_dotenv

userWithRoots = [502643682]
load_dotenv()
token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)
conn = sqlite3.connect('newUsers.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY autoincrement,
   idtelegram TEXT,
   startdate DATE);
 """)
conn.commit()


def insertsql(entity):
    cur.execute('INSERT INTO users(idtelegram,startdate) VALUES(?,?)', entity)

def selectidsql():
    cur.execute('SELECT idtelegram FROM users')
    return cur.fetchall()

def selectdates(sql):
    cur.execute()

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

@bot.message_handler(commands=['test'])
def test(message):
    list_of_users = selectidsql()
    for user in list_of_users:
        bot.send_message(user[0],"Hello")

def check_dates():




bot.polling(non_stop=True)
