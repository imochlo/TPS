from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import PhotoImage
from PIL import ImageTk, Image
import tkinter as tk

import sqlite3
import time
import datetime
import os

class Local():
    def __init__ (self, master):
        self.SCRN_W, self.SCRN_H = master.winfo_screenwidth(), master.winfo_screenheight()

    def setFullScreen(self, window):
        window.geometry("%dx%d" % (self.SCRN_W, self.SCRN_H))

    def percentScreenW(self, value):
        return round(value*0.01*self.SCRN_W)

    def percentScreenH(self, value):
        return round(value*0.01*self.SCRN_H)

    def getCWD(self):
        return os.getCWD()
    
    def getTimeNow(self):
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def getDateNow(self):
        return str(datetime.datetime.now().strftime('%Y-%m-%d'))

class Db():
    def __init__ (self):
        self.dbPath = "db/TPS.db"

    def get(self, text_command):
        db_conn = sqlite3.connect(self.dbPath)
        db_crsr = db_conn.cursor()
        db_crsr.execute(text_command)
        return db_crsr.fetchall()
    
    def set(self, text_command):
        db_conn = sqlite3.connect(self.dbPath)
        db_crsr = db_conn.cursor()
        db_crsr.execute(text_command)
        db_conn.commit()
        db_conn.close()

if __name__ == "__main__":
    pass
