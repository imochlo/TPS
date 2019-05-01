#!/usr/bin/python
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import PhotoImage
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import time
import os

CWD=os.getcwd()

class ReportsWindow():
    def __init__ (self, master):
        master.title("TPSys Reports")

        self.init_backBtn(master)

        self.frame1 = Frame(master, background="red")
        self.frame1.pack(side=TOP, fill=X)
        self.init_filter(self.frame1)

        self.frame2 = Frame(master, background="blue")
        self.frame2.pack(side=TOP, fill=X)
        self.init_reportBtns(self.frame2)

        self.frame3 = Frame(master, background="yellow")
        self.frame3.pack(side=TOP, fill=BOTH, expand=True)

        #setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=percentSCRNH(0.3))
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_filter(self,master):
        monthList = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dayList = ["", 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        yearList = ["", 2018, 2019, 2020, 2021]

        self.filterFrame=Frame(master)
        self.filterFrame.pack(anchor=W)

        self.mid1=Frame(self.filterFrame)
        self.mid1.pack(anchor=W)
        
        repGen = IntVar()
        self.rdbtn1 = Radiobutton(self.mid1, text="Generate Today    ", value=1, variable=repGen)
        self.rdbtn1.grid(column=0, row=0)
        self.rdbtn2 = Radiobutton(self.mid1, text="Generate Duration", value=2, variable=repGen)
        self.rdbtn2.grid(column=0, row=1)
        self.rdbtn2 = Radiobutton(self.mid1, text="Generate Duration", value=2, variable=repGen)

        self.lblStartMonth = Label(self.mid1, text="Start Date:")
        self.lblStartMonth.grid(column=0, row=2, sticky=E)

        self.cbStartMonth = ttk.Combobox(self.mid1, width=15)
        self.cbStartMonth['values'] = monthList
        self.cbStartMonth.current(0)
        self.cbStartMonth.grid(column=1, row=2, padx=10)

        self.cbStartDay = ttk.Combobox(self.mid1, width=5)
        self.cbStartDay['values'] = dayList
        self.cbStartDay.current(0)
        self.cbStartDay.grid(column=2, row=2, padx=10)

        self.cbStartYear = ttk.Combobox(self.mid1, width=10)
        self.cbStartYear['values'] = yearList
        self.cbStartYear.current(0)
        self.cbStartYear.grid(column=3, row=2, padx=10)

        self.lblEndMonth = Label(self.mid1, text="End Date:")
        self.lblEndMonth.grid(column=0, row=3, sticky=E)

        self.cbEndMonth = ttk.Combobox(self.mid1, width=15)
        self.cbEndMonth['values'] = monthList
        self.cbEndMonth.current(0)
        self.cbEndMonth.grid(column=1, row=3, padx=10)

        self.cbEndDay = ttk.Combobox(self.mid1, width=5)
        self.cbEndDay['values'] = dayList
        self.cbEndDay.current(0)
        self.cbEndDay.grid(column=2, row=3, padx=10)

        self.cbEndYear = ttk.Combobox(self.mid1, width=10)
        self.cbEndYear['values'] = yearList
        self.cbEndYear.current(0)
        self.cbEndYear.grid(column=3, row=3, padx=10)
        
    def init_reportBtns(self, frame):
        self.btnFrame=Frame(frame)
        self.btnFrame.pack(anchor=W)

        self.genBtn = Button(self.btnFrame, text="Generate Sales Report")
        self.genBtn.grid(column=0, row=0)

        self.genBtn = Button(self.btnFrame, text="Generate Orders Report")
        self.genBtn.grid(column=1, row=0)

        self.genBtn = Button(self.btnFrame, text="Generate Customers Report")
        self.genBtn.grid(column=2, row=0)

        print(time.time())

    def generate_list(self,master,db_command):
        self.reportFrame = Frame(master)
        self.reportFrame.pack(side=BOTTOM, expand=True, fill=Y, pady=200)

        self.reportTree = ttk.Treeview(self.reportFrame, column=("no","cat","name","price","edit","rm"), show='headings', padding=50)

    def generate_list(self,master,db_command):
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

def percentSCRNW(value):
    return round(value*0.01*SCRN_W)

def percentSCRNH(value):
    return round(value*0.01*SCRN_H)

root = Tk()
SCRN_W, SCRN_H = root.winfo_screenwidth(), root.winfo_screenheight()
root.bind("<Control-w>", quit)
root.geometry("%dx%d" % (percentSCRNW(70), percentSCRNH(70)))

#startup = StartupWindow(root)
#menu = MenuWindow(root)
reports = ReportsWindow(root)
root.mainloop()
