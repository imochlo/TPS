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
class MenuWindow():
    def __init__ (self, master):
        master.title("TPSys Menu")
        self.init_backBtn(master)

        self.frame1 = Frame(master, background="red")
        self.frame1.pack(side=TOP, fill=BOTH, expand=True)
        self.generate_menuTree(self.frame1)

        #setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=percentSCRNH(0.3))
        self.btnBack.pack(side=TOP, fill=BOTH)
    
    def init_fileMenu(self, master):
        self.file_item = Menu(master, tearoff=0)
        self.file_item.add_command(label='Add Item')

        self.file_list = Menu(master)
        self.file_list.add_cascade(label='File', menu=self.file_item)
        master.config(menu=self.file_list)

    def generate_menuTree(self,frame):
        no_index=0
        name_index=1
        cat_index=2
        price_index=3
        image_index=4

        self.menuFrame = Frame(frame)
        self.menuFrame.pack(expand=True, fill=BOTH, pady=100, padx=100)

        self.menuTree = ttk.Treeview(self.menuFrame, column=("no","cat","name","price","edit","rm"), show='headings')

        self.menuTree.column("no", width=20, anchor=CENTER)
        self.menuTree.column("cat", width=150)
        self.menuTree.column("name", width=300)
        self.menuTree.column("price", width=100, anchor=CENTER)
        self.menuTree.column("edit", width=100, anchor=CENTER)
        self.menuTree.column("rm", width=100, anchor=CENTER)

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

        self.results = getListFromDb("SELECT * FROM menu")

        self.menuTree.insert("", tk.END, text="addItemRow", value=("","","","","","Add Item"))
        for row in self.results:

            _values = [row[no_index], row[cat_index], row[name_index], row[price_index], "Edit this", "Remove this"]

            self.menuTree.insert("", tk.END, row[0], value=_values)
            ttk.Style().configure("Treeview", rowheight=50)

        self.menuTree.insert("", tk.END, text="addItemRow", value=("","","","","","Add Item"))

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
menu = MenuWindow(root)
#reports = ReportsWindow(root)
root.mainloop()
