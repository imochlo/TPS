#!/usr/bin/python
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import PhotoImage
from PIL import ImageTk, Image
import tkinter as tk

import sqlite3
import time
import os

import Services

class DashboardWindow():
    def __init__ (self, master):
        self.master=master
        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Dashboard")

        self.init_catList()

        self.init_backBtn(master)

        self.frame2 = Frame(master, background="red")
        self.frame2.pack(side=TOP, fill=BOTH, expand=True)
        self.init_tableTree(self.frame2)
        self.genTableTree()

        self.frame3 = Frame(master, background="blue")
        self.frame3.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_catBtn(self.frame3)

        self.frame4 = Frame(master, background="white")
        self.frame4.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_catTree(self.frame4)

        self.frame5 = Frame(master, background="yellow")
        self.frame5.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_billTree(self.frame5)

        self.frame6 = Frame(master, background="green")
        self.frame6.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_billBtn(self.frame6)
        
        self.pc.setFullScreen(master)


    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2, command=self.master.destroy)
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_tableTree(self, frame):
        name_index=1
        price_index=3

        self.tableFrame=Frame(frame)
        self.tableFrame.pack(expand=True, fill=BOTH, pady=30, padx=20)

        self.tableTree = ttk.Treeview(self.tableFrame, column=("no", "tableNo", "partySize", "coPref", "qty", "totAmt", "select"    ), show='headings')
        ttk.Style().configure("Treeview", rowheight=50)

        self.tableTree.column("no", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("tableNo", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("partySize", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("coPref", width=self.pc.percentScreenW(20), stretch=True, anchor=CENTER)
        self.tableTree.column("qty", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
        self.tableTree.column("totAmt", width=self.pc.percentScreenW(20), stretch=True, anchor=CENTER)
        self.tableTree.column("select", width=self.pc.percentScreenW(25), stretch=True, anchor=CENTER)
        
        self.tableTree.heading("no", text="")
        self.tableTree.heading("tableNo", text="Table No.")
        self.tableTree.heading("partySize", text="No. of Guests")
        self.tableTree.heading("coPref", text="Checkout Preference")
        self.tableTree.heading("qty", text="Items Ordered")
        self.tableTree.heading("totAmt", text="Total Balance")
        self.tableTree.heading("select", text="")

        self.tableTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.tableScroll = ttk.Scrollbar(self.tableFrame, orient=VERTICAL, command=self.tableTree.yview)
        self.tableScroll.pack(side=RIGHT, fill=Y)
        self.tableTree.configure(yscrollcommand=self.tableScroll.set)

        self.tableTree.bind("<Button-1>", self.tableProcessClick)

    def init_catTree(self, frame):
        name_index=1
        price_index=3

        self.foodFrame=Frame(frame)
        self.foodFrame.pack(expand=True, fill=BOTH, padx=20, pady=30)

        self.catTree = ttk.Treeview(self.foodFrame, column=("name", "price", "add"), show='headings', selectmode="extended")
        
        self.catTree.column("name", width=self.pc.percentScreenW(10), stretch=True)
        self.catTree.column("price", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.catTree.column("add", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        
        self.catTree.heading("name", text="Name")
        self.catTree.heading("price", text="Price", anchor=CENTER)
        self.catTree.heading("add", text="", anchor=CENTER)
        self.catTree.grid(column=0, row=0, sticky=NSEW)

        self.catScroll = ttk.Scrollbar(self.foodFrame, orient=VERTICAL, command=self.catTree.yview)
        self.catScroll.grid(column=1, row=0, sticky=NS)
        self.catTree.configure(yscrollcommand=self.catScroll.set)
        self.catTree.delete(*self.catTree.get_children())

    def init_billTree(self, frame):
        name_index=1
        price_index=3

        self.billFrame=Frame(frame)
        self.billFrame.pack(expand=True, fill=BOTH, pady=30, padx=20)

        self.billTree = ttk.Treeview(self.billFrame, column=("no", "name", "price", "add", "qty", "rm"), show='headings')
        
        self.billTree.column("no", width=self.pc.percentScreenW(5), stretch=True)
        self.billTree.column("name", width=self.pc.percentScreenW(20), stretch=True)
        self.billTree.column("price", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.billTree.column("add", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.billTree.column("qty", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.billTree.column("rm", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        
        self.billTree.heading("no", text="")
        self.billTree.heading("name", text="Name")
        self.billTree.heading("price", text="Price")
        self.billTree.heading("rm", text="Remove")
        self.billTree.heading("qty", text="Qty")
        self.billTree.heading("add", text="Add")

        self.billTree.grid(column=0, row=0, sticky=NSEW)


        self.billScroll = ttk.Scrollbar(self.billFrame, orient=VERTICAL, command=self.billTree.yview)
        self.billScroll.grid(column=1, row=0, sticky=NS)
        self.billTree.configure(yscrollcommand=self.billScroll.set)
        self.billTree.delete(*self.billTree.get_children())

    def init_billBtn(self, frame):
        self.billoutFrame=Frame(frame)
        self.billoutFrame.pack(expand=True, padx=30)
        self.billBtn=Button(self.billoutFrame, text="Bill Out", height=3, width=7, background="green", foreground="white", font='bold')
        self.billBtn.grid(column=0, row=0)
        self.cancelBtn=Button(self.billoutFrame, text="Cancel", height=3, width=7, background="red", foreground="white", font='bold')
        self.cancelBtn.grid(column=0, row=1)

    def init_catBtn(self, frame):
        self.catFrame=Frame(frame)
        self.catFrame.pack(expand=True, padx=30)
        row_num=0

        for i in range(len(self.catList)):
            elem = self.catList[i]
            self.btn = Button(self.catFrame, text=self.catList[i], width=10, height=2, command=lambda cat=elem:self.genCatTree(cat))
            if (i%2==0):
                self.btn.grid(row=row_num, column=0, padx=5, pady=5)
            else:
                self.btn.grid(row=row_num, column=1, padx=5, pady=5)
                row_num+=1

    def init_catList(self):
        dbResults = self.db.get("SELECT DISTINCT category FROM menu")
        self.catList = []

        for elem in dbResults:
            self.catList.append(elem[0])

    def genTableTree(self):
        self.tableTree.delete(*self.tableTree.get_children())

        self.tableResults = self.db.get("SELECT transactions.orderNo, customer.tableNo, customer.partySize, customer.checkoutPref, sum(foodOrders.qty), invoice.totAmt FROM foodOrders LEFT JOIN transactions ON foodOrders.orderNo=transactions.OrderNo INNER JOIN customer ON transactions.custNo=customer.custNo INNER JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.rcvAmt IS NULL GROUP BY foodOrders.orderNo")

        rowInc=1
        self.tableTree.insert("", tk.END, values=("", "", "", "", "", "", "Add Table"))
        for row in self.tableResults:
            _values=[rowInc, row[1], row[2], row[3], row[4], row[5], "Select"]
            rowInc+=1
            self.tableTree.insert("", tk.END, row[0], values=_values)

        self.tableTree.insert("", tk.END, values=("", "", "", "", "", "", "Add Table"))
        ttk.Style().configure("Treeview", rowheight=30)

    def genCatTree(self, cat):
        name_index=1
        price_index=3

        self.catTree.delete(*self.catTree.get_children())
        results=self.db.get("SELECT * FROM menu WHERE category = \"%s\" " % cat)

        for row in results:
            _values=[row[name_index], row[price_index], "add"]
            self.catTree.insert("", tk.END, row[0], values=_values)

    def tableProcessClick(self, event):
        item = self.tableTree.identify('item', event.x, event.y)
        row = self.tableTree.identify_row(event.y)
        col = self.tableTree.identify_column(event.x)

        self.billTree.delete(*self.billTree.get_children())

        if any(row == str(elem[0]) for elem in self.tableResults):
            self.billResults = self.db.get("SELECT foodOrders.orderNo, menu.name, menu.price, foodOrders.qty FROM foodOrders LEFT JOIN menu ON foodOrders.menuNo=menu.menuNo WHERE foodOrders.orderNo=%s" % row)
            print(self.billResults) 

        rowInc=1
        for row in self.billResults:
            _values=[rowInc, row[1], row[2], "-", row[3], "+"]
            self.billTree.insert("", tk.END, row[1], values=_values)

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    dashboard = DashboardWindow(root)
    root.mainloop()
