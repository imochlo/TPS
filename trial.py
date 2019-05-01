from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
import sqlite3
from PIL import ImageTk, Image
import datetime
import os 

print(os.getcwd())

def getListFromDb(text_command):
    db_conn = sqlite3.connect("db/TPSys.db")
    db_crsr = db_conn.cursor()
    db_crsr.execute(text_command)
    return db_crsr.fetchall()

def addIntoDb(arg1, arg2):
    db_conn = sqlite3.connect("db/TPSys.db")
    db_crsr = db_conn.cursor()
    db_crsr.execute('''INSERT INTO test VALUES (?,?)''', (arg1, arg2))
    db_conn.commit()
    db_conn.close()

results = getListFromDb("SELECT * FROM menu")
print(len(results))

for element in results:
    print(element)

print(os.getcwd()+results[0][4])

now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now)
addIntoDb(now, now)
_list = getListFromDb("SELECT strftime('%M', dt1) FROM test")
print(_list)
