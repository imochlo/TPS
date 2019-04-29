#!/usr/bin/python
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3

class StartupWindow():

    PAD_FRBTN_X = 40
    PAD_FRBTN_Y = 40
    PAD_FRLB_X = 30
    PAD_FRLB_Y = [10,40]
    BTN_HEIGHT = 5
    BTN_WIDTH = 10

    def __init__ (self, master):
        master.title("TPSys")
        self.init_label(master)
        self.init_buttons(master)

    def init_label(self, master):
        self.lblFrame = Frame(master)
        self.lblFrame.pack(side=BOTTOM, padx=self.PAD_FRLB_X, pady=self.PAD_FRLB_Y)
        self.lblMain = Label(self.lblFrame, text = "Welcome to TPSys. Hover over a task.")
        self.lblMain.pack()

    def init_buttons(self, frame):
        self.btnFrame = Frame(frame)
        self.btnFrame.pack(padx=self.PAD_FRBTN_X, pady=self.PAD_FRBTN_Y)

        self.btnDashboard = Button(self.btnFrame, text = "Dashboard", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT)
        self.btnDashboard.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnDashboard.bind('<Enter>', lambda event: self.lblMain.configure(text="Input new transactions in the dashboard"))
        self.btnDashboard.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))

        #menu
        self.btnMenu = Button(self.btnFrame, text = "Menu" , justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, command=setFullScreen)
        self.btnMenu.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnMenu.bind('<Enter>', lambda event: self.lblMain.configure(text="Add or edit menu items"))
        self.btnMenu.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))

        self.btnReports = Button(self.btnFrame, text = "Reports", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT)
        self.btnReports.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnReports.bind('<Enter>', lambda event: self.lblMain.configure(text="Generate or view sales, customer, or order reports"))
        self.btnReports.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))


class MenuWindow():
    def __init__ (self, master):
        setFullScreen(master)
        master.title("TPSys Menu")
        self.init_backToMain(master)

    def init_backToMain(self, master):
        self.topFrame = Frame(master)
        self.topFrame.pack(side=TOP)
        self.btnBack = Button(self.topFrame, text="Back to main window", width=SCRN_W, height =2)
        self.btnBack.pack()

        results = getListFromDb("SELECT * FROM menu")
        for i in results:
            print(i)
    
    def init_filter(self, master):
        pass
    
    def init_sorter(self, master):
        pass


def quit(event):
        root.quit()

def setFullScreen(window):
    window.geometry("%dx%d" % (SCRN_W, SCRN_H))

def getListFromDb(text_command):
    db_conn = sqlite3.connect("db/TPSys.db")
    db_crsr = db_conn.cursor()
    db_crsr.execute(text_command)
    return db_crsr.fetchall()

root = Tk()
SCRN_W, SCRN_H = root.winfo_screenwidth(), root.winfo_screenheight()
root.bind("<Control-w>", quit)

#startup = StartupWindow(root)
menu = MenuWindow(root)
root.mainloop()
