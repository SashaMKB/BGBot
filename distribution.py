import pandas
import sqlite3

conn = sqlite3.connect('newUsers.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY autoincrement,
   login TEXT,
   startdate DATE);
 """)
conn.commit()

excel_data_df = pandas.read_excel('D:\\NewersBG.xlsx')
login_list = excel_data_df["Login"].tolist()
date_list = excel_data_df["Start Date"].tolist()

def insertsql(entity):
    cur.execute('INSERT INTO users(login,startdate) VALUES(?,?)', entity)


for login, date in zip(login_list, date_list):
    entity = (login, date)
    insertsql(entity)

conn.commit()
