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
category_list=["Appetizers", "Soup", "Salad", "Sandwiches", "Pasta", "Entree", "Soda", "Coolers", "Platter"] 

class DashboardWindow():
    def __init__ (self, master):
        master.title("TPSys Dashboard")

        self.init_backBtn(master)

        self.frame2 = Frame(master, background="red")
        self.frame2.pack(side=TOP, fill=BOTH, expand=True)
        self.generate_tableTree(self.frame2)

        self.frame3 = Frame(master, background="blue")
        self.frame3.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_catBtn(self.frame3)

        self.frame4 = Frame(master, background="white")
        self.frame4.pack(side=LEFT, fill=BOTH, expand=True)
        self.generate_catTree(self.frame4)

        self.frame5 = Frame(master, background="yellow")
        self.frame5.pack(side=LEFT, fill=BOTH, expand=True)
        self.generate_billTree(self.frame5)

        self.frame6 = Frame(master, background="green")
        self.frame6.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_billBtn(self.frame6)
        
        #setFullScreen(master)


    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2)
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_tableTree(self, frame):
        pass

    def generate_tableTree(self, frame):
        name_index=1
        price_index=3

        self.tableFrame=Frame(frame)
        self.tableFrame.pack(expand=True,fill=BOTH, pady=30, padx=20)

        self.tableTree = ttk.Treeview(self.tableFrame, column=("name", "price", "add"), show='headings')
        
        self.tableTree.column("name", width=200, stretch=TRUE)
        self.tableTree.column("price", width=100, anchor=CENTER)
        self.tableTree.column("add", width=75, anchor=CENTER)
        
        self.tableTree.heading("name", text="Name")
        self.tableTree.heading("price", text="Price", anchor=CENTER)
        self.tableTree.heading("add", text="", anchor=CENTER)
        self.tableTree.pack(side=LEFT,expand=True, fill=BOTH)

        self.tableScroll = ttk.Scrollbar(self.tableFrame, orient=VERTICAL, command=self.tableTree.yview)
        self.tableScroll.pack(side=RIGHT, fill=Y)
        self.tableTree.configure(yscrollcommand=self.tableScroll.set)
        self.tableTree.delete(*self.tableTree.get_children())

        self.results=getListFromDb("SELECT * FROM menu WHERE category='Appetizers'") 

        for row in self.results:
            _values=[row[name_index], row[price_index], "add"]
            self.tableTree.insert("", tk.END, row[0], values=_values)
            ttk.Style().configure("Treeview", rowheight=30)

    def generate_catTree(self, frame):
        name_index=1
        price_index=3

        self.foodFrame=Frame(frame)
        self.foodFrame.pack(expand=True,fill=BOTH, padx=20, pady=30)

        self.catTree = ttk.Treeview(self.foodFrame, column=("name", "price", "add"), show='headings')
        
        self.catTree.column("name", width=200, stretch=TRUE)
        self.catTree.column("price", width=100, anchor=CENTER)
        self.catTree.column("add", width=75, anchor=CENTER)
        
        self.catTree.heading("name", text="Name")
        self.catTree.heading("price", text="Price", anchor=CENTER)
        self.catTree.heading("add", text="", anchor=CENTER)
        self.catTree.pack(side=LEFT,expand=True, fill=BOTH)

        self.catScroll = ttk.Scrollbar(self.foodFrame, orient=VERTICAL, command=self.catTree.yview)
        self.catScroll.pack(side=RIGHT, fill=Y)
        self.catTree.configure(yscrollcommand=self.catScroll.set)
        self.catTree.delete(*self.catTree.get_children())

        self.results=getListFromDb("SELECT * FROM menu WHERE category='Appetizers'") 
        print(self.results)

        for row in self.results:
            _values=[row[name_index], row[price_index], "add"]
            self.catTree.insert("", tk.END, row[0], values=_values)
            ttk.Style().configure("Treeview", rowheight=30)

    def generate_billTree(self, frame):
        name_index=1
        price_index=3

        self.billFrame=Frame(frame)
        self.billFrame.pack(expand=True,fill=BOTH, pady=30, padx=20)

        self.billTree = ttk.Treeview(self.billFrame, column=("name", "price", "add"), show='headings')
        
        self.billTree.column("name", width=200, stretch=TRUE)
        self.billTree.column("price", width=100, anchor=CENTER)
        self.billTree.column("add", width=75, anchor=CENTER)
        
        self.billTree.heading("name", text="Name")
        self.billTree.heading("price", text="Price", anchor=CENTER)
        self.billTree.heading("add", text="", anchor=CENTER)
        self.billTree.pack(side=LEFT,expand=True, fill=BOTH)

        self.billScroll = ttk.Scrollbar(self.billFrame, orient=VERTICAL, command=self.billTree.yview)
        self.billScroll.pack(side=RIGHT, fill=Y)
        self.billTree.configure(yscrollcommand=self.billScroll.set)
        self.billTree.delete(*self.billTree.get_children())

        self.results=getListFromDb("SELECT * FROM menu WHERE category='Appetizers'") 
        print(self.results)

        for row in self.results:
            _values=[row[name_index], row[price_index], "add"]
            self.billTree.insert("", tk.END, row[0], values=_values)
            ttk.Style().configure("Treeview", rowheight=30)

    def init_billBtn(self, frame):
        self.billoutFrame=Frame(frame)
        self.billoutFrame.pack(expand=True, padx=30)
        self.billBtn=Button(self.billoutFrame, text="Bill Out")
        self.billBtn.grid(column=0, row=0)
        self.cancelBtn=Button(self.billoutFrame, text="Cancel")
        self.cancelBtn.grid(column=0, row=1)

    def init_catBtn(self, frame):
        self.catFrame=Frame(frame)
        self.catFrame.pack(expand=True, padx=30)
        row_num=0
        for i in range(len(category_list)):
            self.btn = Button(self.catFrame, text=category_list[i], width=10, height=2, command=lambda cat=category_list[i]:self.gen_category(cat))
            if (i%2==0):
                self.btn.grid(row=row_num, column=0, padx=5, pady=5)
            else:
                self.btn.grid(row=row_num, column=1, padx=5, pady=5)
                row_num+=1

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

dashboard = DashboardWindow(root)
root.mainloop()
