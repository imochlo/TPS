#!/usr/bin/python
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import PhotoImage
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import tkinter as tk

import sqlite3
import time
import os

import Services

no_index = 0
date_index = 1
discount_index = 2
og_index = 3
tot_index = 4
rcv_index = 5

class ReportsWindow():
    def __init__ (self, master):
        self.pc = Services.Local(master)
        self.db = Services.Db()

        master.bind("<Control-w>", lambda event: master.destroy())
        master.title("TPSys Reports")

        frame = Frame(master, background="black")
        frame.pack(side=TOP, fill=X)
        self.init_backBtn(frame)

        frame = Frame(master, background="black")
        frame.pack(side=TOP, fill=X, pady=50, padx=100)
        self.init_filter(frame)
        self.init_reportBtns(frame)

        self.treeFrame = Frame(master, background="yellow")
        self.treeFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.init_reportTree()

        self.pc.setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2)
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_filter(self,master):
        self.filterFrame=Frame(master)
        self.filterFrame.pack(anchor=W)

        self.durationOpt = IntVar()
        self.rdbtn1 = Radiobutton(self.filterFrame, text="Generate Today", value=1, variable=self.durationOpt)
        self.rdbtn1.grid(column=0, row=0, sticky=W)
        self.rdbtn1.select()

        self.rdbtn2 = Radiobutton(self.filterFrame, text="Generate Duration", value=2, variable=self.durationOpt)
        self.rdbtn2.grid(column=0, row=1, sticky=W)

        self.lblStartMonth = Label(self.filterFrame, text="Start Date:")
        self.lblStartMonth.grid(column=0, row=2, sticky=E)

        self.dateStart = DateEntry(self.filterFrame)
        self.dateStart.grid(column=1, row=2)

        self.lblEndMonth = Label(self.filterFrame, text="End Date:")
        self.lblEndMonth.grid(column=0, row=3, sticky=E)

        self.dateEnd = DateEntry(self.filterFrame)
        self.dateEnd.grid(column=1, row=3)

    def init_reportBtns(self, frame):
        self.btnFrame=Frame(frame)
        self.btnFrame.pack(anchor=W, pady=10)

        self.genBtn = Button(self.btnFrame, text="Generate Sales Report", command=self.genSalesRep)
        self.genBtn.pack(side=LEFT, padx=[0,20])

        self.genBtn = Button(self.btnFrame, text="Generate Orders Report", command=self.genOrdersRep)
        self.genBtn.pack(side=LEFT, padx=[0,20])

        self.genBtn = Button(self.btnFrame, text="Generate Customers Report", command=self.genCustomersRep)
        self.genBtn.pack(side=LEFT)

    def init_reportTree(self):
        self.reportFrame = Frame(self.treeFrame)
        self.reportFrame.pack(expand=True, fill=BOTH, pady=100, padx=100)

        self.reportTree = ttk.Treeview(self.reportFrame, show='headings')
        self.reportTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.reportFrame, orient=VERTICAL, command=self.reportTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)

        self.reportTree.configure(yscrollcommand=self.scrollBar.set)

    def genSalesRep(self):
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT * FROM invoice WHERE date = \"%s\"" % dateNow
        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT * FROM invoice WHERE date BETWEEN \"%s\"  AND \"%s\"" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "date", "or", "ogPrice", "discount", "totPrice", "rcvAmt")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("date", width=150, anchor=CENTER, stretch=False)
        self.reportTree.column("or", width=200, anchor=CENTER, stretch=False)
        self.reportTree.column("ogPrice", width=150, anchor=CENTER, stretch=False)
        self.reportTree.column("discount", width=100, anchor=CENTER, stretch=False)
        self.reportTree.column("totPrice", width=150, anchor=CENTER, stretch=False)
        self.reportTree.column("rcvAmt", width=150, anchor=CENTER, stretch=False)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("date", text="Date")
        self.reportTree.heading("or", text="OR No.")
        self.reportTree.heading("ogPrice", text="Original Price")
        self.reportTree.heading("discount", text="Discount")
        self.reportTree.heading("totPrice", text="Total Price")
        self.reportTree.heading("rcvAmt", text="Received Amount")

        ttk.Style().configure("Treeview", rowheight=50)
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        sumRcv=0
        for row in self.dbResults:
            _values = [listInc, row[date_index], row[no_index], row[og_index], row[discount_index], row[tot_index], row[rcv_index]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1
            sumRcv+=row[rcv_index]

        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "", ""])
        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "# of Transactions:", len(self.dbResults)])
        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "Total Received:", sumRcv])

    def genOrdersRep(self):
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT menu.category, menu.name, sum(qty) FROM foodOrders inner join menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.orderNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date = \"%s\" GROUP BY menu.menuNo ORDER BY menu.category" % (dateNow)
        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT menu.category, menu.name, sum(qty) FROM foodOrders inner join menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.orderNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date BETWEEN \"%s\" AND \"%s\" GROUP BY menu.menuNo ORDER BY menu.category" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "cat", "name", "qty")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("cat", width=200, anchor=CENTER, stretch=False)
        self.reportTree.column("name", width=500, anchor=CENTER, stretch=False)
        self.reportTree.column("qty", width=350, anchor=CENTER, stretch=False)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("cat", text="Category")
        self.reportTree.heading("name", text="Name")
        self.reportTree.heading("qty", text="Quantity Sold")

        ttk.Style().configure("Treeview", rowheight=50)
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        for row in self.dbResults:
            _values = [listInc, row[0], row[1], row[2]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1

    def genCustomersRep(self):
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT customer.arrTime, customer.deptTime, customer.partySize, customer.checkoutPref, sum(foodOrders.qty) FROM foodOrders LEFT JOIN transactions ON foodOrders.orderNo=transactions.orderNo LEFT JOIN customer ON transactions.custNo=customer.custNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date IS NOT NULL AND invoice.date = \"%s\" GROUP BY foodOrders.orderNo" % dateNow
        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT customer.arrTime, customer.deptTime, customer.partySize, customer.checkoutPref, sum(foodOrders.qty) FROM foodOrders LEFT JOIN transactions ON foodOrders.orderNo=transactions.orderNo LEFT JOIN customer ON transactions.custNo=customer.custNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date IS NOT NULL AND invoice.date BETWEEN \"%s\" AND \"%s\" GROUP BY foodOrders.orderNo" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "arrTime", "deptTime", "partySize", "checkoutPref", "orderSum")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("arrTime", width=200, anchor=CENTER, stretch=False)
        self.reportTree.column("deptTime", width=500, anchor=CENTER, stretch=False)
        self.reportTree.column("partySize", width=350, anchor=CENTER, stretch=False)
        self.reportTree.column("checkoutPref", width=350, anchor=CENTER, stretch=False)
        self.reportTree.column("orderSum", width=350, anchor=CENTER, stretch=False)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("arrTime", text="Arrival Time")
        self.reportTree.heading("deptTime", text="Departure Time")
        self.reportTree.heading("partySize", text="Size of Party")
        self.reportTree.heading("checkoutPref", text="Checkout Preference")
        self.reportTree.heading("orderSum", text="Number of Orders")

        ttk.Style().configure("Treeview", rowheight=50)
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        for row in self.dbResults:
            _values = [listInc, row[0], row[1], row[2], row[3], row[4]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    reports = ReportsWindow(root)
    root.mainloop()
