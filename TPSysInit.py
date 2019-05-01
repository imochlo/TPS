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
        self.init_backBtn(master)
        self.generate_list(master, "SELECT * FROM menu")

    def init_backToMain(self, master):
        pass

        #results = getListFromDb("SELECT * FROM menu")
        #imageLink=results[20][4]

        #self.img=Image.open(CWD+imageLink)
        #self.img.thumbnail((200,200), Image.ANTIALIAS)
        #self.render = ImageTk.PhotoImage(self.img)
        #self.panel = Label(master, image=self.render)
        #self.panel.pack(side=LEFT)

    def init_backBtn(self, master):
        self.topFrame = Frame(master)
        self.topFrame.pack(side=TOP)
        self.btnBack = Button(self.topFrame, text="Back to main window", width=SCRN_W, height =2)
        self.btnBack.pack()
    
    def init_fileMenu(self, master):
        self.file_item = Menu(master, tearoff=0)
        self.file_item.add_command(label='Add Item')

        self.file_list = Menu(master)
        self.file_list.add_cascade(label='File', menu=self.file_item)
        master.config(menu=self.file_list)

    def init_filter(self, master):
        pass
    
    def init_sorter(self, master):
        pass

    def generate_list(self,master, db_command):
        no_index=0
        name_index=1
        cat_index=2
        price_index=3
        image_index=4

        self.menuFrame = Frame(master)
        self.menuFrame.pack(expand=True, fill=Y, pady=200)

        self.menuTree = ttk.Treeview(self.menuFrame, column=("no","cat","name","price","edit","rm"), show='headings', padding=50)

        self.menuTree.column("no", width=50)
        self.menuTree.column("cat", width=200)
        self.menuTree.column("name", width=500, stretch=TRUE)
        self.menuTree.column("price", width=100, anchor=CENTER)
        self.menuTree.column("edit", width=200, anchor=CENTER)
        self.menuTree.column("rm", width=200, anchor=CENTER)

        self.menuTree.heading("no", text="No.")
        self.menuTree.heading("cat", text="Category")
        self.menuTree.heading("name", text="Name")
        self.menuTree.heading("price", text="Price")
        self.menuTree.heading("edit", text="Edit")
        self.menuTree.heading("rm", text="Add/Remove")
        self.menuTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.menuFrame, orient=VERTICAL, command=self.menuTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.menuTree.configure(yscrollcommand=self.scrollBar.set)
        self.menuTree.delete(*self.menuTree.get_children())

        self.results = getListFromDb(db_command)
        self.menuTree.insert("", tk.END, text="addItemRow", value=("","","","","","Add Item"))
        for row in self.results:

            #self.img=Image.open(CWD+row[image_index])
            #self.img.thumbnail((200,200), Image.ANTIALIAS)
            #self.render = ImageTk.PhotoImage(self.img)

            _values = [row[no_index], row[cat_index], row[name_index], row[price_index], "Edit this", "Remove this"]

            #self.menuTree.insert("", tk.END, row[0], image=self.render, value=_values)
            self.menuTree.insert("", tk.END, row[0], value=_values)
            ttk.Style().configure("Treeview", rowheight=50)

class ReportsWindow():
    def __init__ (self, master):
        setFullScreen(master)
        master.title("TPSys Reports")
        self.init_backBtn(master)
        self.init_filter(master)
        self.generate_list(master, "")

    def init_backBtn(self, master):
        self.topFrame = Frame(master)
        self.topFrame.pack(side=TOP)

        self.btnBack = Button(self.topFrame, text="Back to main window", width=SCRN_W, height =2)
        self.btnBack.pack()

    def init_filter(self,master):
        monthList = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dayList = ["", 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        yearList = ["", 2018, 2019, 2020, 2021]

        self.midFrame=Frame(master)
        self.midFrame.pack(anchor=W, padx=100, pady=50)

        self.mid1=Frame(self.midFrame)
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
        
        self.mid2=Frame(self.midFrame)
        self.mid2.pack(anchor=W, pady=20)

        self.genBtn = Button(self.mid2, text="Generate Sales Report")
        self.genBtn.grid(column=0, row=0)

        self.genBtn = Button(self.mid2, text="Generate Orders Report")
        self.genBtn.grid(column=1, row=0)

        self.genBtn = Button(self.mid2, text="Generate Customers Report")
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

root = Tk()
SCRN_W, SCRN_H = root.winfo_screenwidth(), root.winfo_screenheight()
root.bind("<Control-w>", quit)

#startup = StartupWindow(root)
#menu = MenuWindow(root)
reports = ReportsWindow(root)
root.mainloop()
