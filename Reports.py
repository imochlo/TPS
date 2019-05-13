#/usr/bin/python
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
        self.master=master
        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Reports")

        frame = Frame(master)
        frame.pack(side=TOP, fill=X)
        self.init_backBtn(frame)

        frame = Frame(master)
        frame.pack(side=TOP, fill=X, pady=50, padx=100)
        self.init_filter(frame)
        self.init_reportBtns(frame)

        self.treeFrame = Frame(master)
        self.treeFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.init_reportTree()

        self.pc.setFullScreen(master)

    def init_backBtn(self, frame):
        btnBack = Button(frame, text="Back to main window", height=2, command=self.master.destroy)
        btnBack.pack(side=TOP, fill=BOTH)

    def init_filter(self,master):
        filterFrame=Frame(master)
        filterFrame.pack(anchor=W)

        self.durationOpt = IntVar()
        rdbtn = Radiobutton(filterFrame, text="Generate Today", value=1, variable=self.durationOpt)
        rdbtn.grid(column=0, row=0, sticky=W)
        rdbtn.select()

        rdbtn = Radiobutton(filterFrame, text="Generate Duration", value=2, variable=self.durationOpt)
        rdbtn.grid(column=0, row=1, sticky=W)

        lbl = Label(filterFrame, text="Start Date:")
        lbl.grid(column=0, row=2, sticky=E)

        self.dateStart = DateEntry(filterFrame)
        self.dateStart.grid(column=1, row=2)

        lbl = Label(filterFrame, text="End Date:")
        lbl.grid(column=0, row=3, sticky=E)

        self.dateEnd = DateEntry(filterFrame)
        self.dateEnd.grid(column=1, row=3)

    def init_reportBtns(self, frame):
        btnFrame=Frame(frame)
        btnFrame.pack(anchor=W, pady=10)

        genBtn = Button(btnFrame, text="Generate Sales Report", command=self.genSalesRep)
        genBtn.pack(side=LEFT, padx=[0,20])

        genBtn = Button(btnFrame, text="Generate Orders Report", command=self.genOrdersRep)
        genBtn.pack(side=LEFT, padx=[0,20])

        genBtn = Button(btnFrame, text="Generate Customers Report", command=self.genCustomersRep)
        genBtn.pack(side=LEFT)

    def init_reportTree(self):
        reportFrame = Frame(self.treeFrame)
        reportFrame.pack(expand=True, fill=BOTH, pady=[0,100], padx=100)

        self.reportTree = ttk.Treeview(reportFrame, show='headings')
        self.reportTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(reportFrame, orient=VERTICAL, command=self.reportTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)

        self.reportTree.configure(yscrollcommand=self.scrollBar.set)
        ttk.Style().configure("Treeview", rowheight=50)

    def genSalesRep(self):
        # SALES REP SET UP
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT date, invoiceNo, ogPrice, discount, totAmt, rcvAmt FROM invoice WHERE date = \"%s\" AND rcvAmt IS NOT NULL" % dateNow
        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT date, invoiceNo, ogPrice, discount, totAmt, rcvAmt FROM invoice WHERE date BETWEEN \"%s\" AND \"%s\" and rcvAmt IS NOT NULL" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "date", "or", "ogPrice", "discount", "totAmt", "rcvAmt")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("date", anchor=CENTER, stretch=True)
        self.reportTree.column("or", anchor=CENTER, stretch=True)
        self.reportTree.column("ogPrice", anchor=CENTER, stretch=True)
        self.reportTree.column("discount", anchor=CENTER, stretch=True)
        self.reportTree.column("totAmt", anchor=CENTER, stretch=True)
        self.reportTree.column("rcvAmt", anchor=CENTER, stretch=True)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("date", text="Date")
        self.reportTree.heading("or", text="OR No.")
        self.reportTree.heading("ogPrice", text="Original Price")
        self.reportTree.heading("discount", text="Discount")
        self.reportTree.heading("totAmt", text="Total Price")
        self.reportTree.heading("rcvAmt", text="Received Amount")

        # SALES REP GENERATION
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        sumRcv=0
        for row in self.dbResults:
            _values = [listInc, row[0], row[1], row[2], row[3], row[4], row[5]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1
            sumRcv+=row[rcv_index]

        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "", ""])
        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "# of Transactions:", len(self.dbResults)])
        self.reportTree.insert("", tk.END, value=["", "", "", "", "", "Total Received:", sumRcv])

    def genOrdersRep(self):
        # ORDER REP SET UP
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT menu.category, menu.name, sum(qty) FROM foodOrders inner join menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date = \"%s\" and invoice.rcvAmt IS NOT NULL GROUP BY menu.menuNo ORDER BY menu.category" % (dateNow)
        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT menu.category, menu.name, sum(qty) FROM foodOrders inner join menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.date BETWEEN \"%s\" AND \"%s\" and invoice.rcvAmt IS NOT NULL GROUP BY menu.menuNo ORDER BY menu.category" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "cat", "name", "qty")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("cat", anchor=CENTER, stretch=True)
        self.reportTree.column("name", anchor=CENTER, stretch=True)
        self.reportTree.column("qty", anchor=CENTER, stretch=True)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("cat", text="Category")
        self.reportTree.heading("name", text="Name")
        self.reportTree.heading("qty", text="Quantity Sold")

        # ORDER REP GENERATION
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        for row in self.dbResults:
            _values = [listInc, row[0], row[1], row[2]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1

    def genCustomersRep(self):
        # CUSTOMER REP SET UP
        if (self.durationOpt.get() == 1):
            dateNow = self.pc.getDateNow()
            command = "SELECT customer.arrTime, customer.deptTime, customer.partySize, customer.checkoutPref, sum(foodOrders.qty), invoice.totAmt FROM foodOrders LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo LEFT JOIN customer ON transactions.custNo=customer.custNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.rcvAmt IS NOT NULL AND invoice.date = \"%s\" GROUP BY foodOrders.orderNo" % dateNow

        else:
            dateStart = str(self.dateStart.get_date())
            dateEnd = str(self.dateEnd.get_date())
            command = "SELECT customer.arrTime, customer.deptTime, customer.partySize, customer.checkoutPref, sum(foodOrders.qty), invoice.totAmt FROM foodOrders LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo LEFT JOIN customer ON transactions.custNo=customer.custNo LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo WHERE invoice.rcvAmt IS NOT NULL AND invoice.date BETWEEN \"%s\" AND \"%s\" GROUP BY foodOrders.orderNo" % (dateStart, dateEnd)

        self.dbResults = self.db.get(command)

        self.reportTree["columns"] = ("no", "arrTime", "deptTime", "partySize", "checkoutPref", "orderSum", "totAmt")

        self.reportTree.column("no", width=50, stretch=False)
        self.reportTree.column("arrTime", anchor=CENTER, stretch=True)
        self.reportTree.column("deptTime", anchor=CENTER, stretch=True)
        self.reportTree.column("partySize", anchor=CENTER, stretch=True)
        self.reportTree.column("checkoutPref", anchor=CENTER, stretch=True)
        self.reportTree.column("orderSum", anchor=CENTER, stretch=True)
        self.reportTree.column("totAmt", anchor=CENTER, stretch=True)

        self.reportTree.heading("no", text="")
        self.reportTree.heading("arrTime", text="Arrival Time")
        self.reportTree.heading("deptTime", text="Departure Time")
        self.reportTree.heading("partySize", text="Size of Party")
        self.reportTree.heading("checkoutPref", text="Checkout Preference")
        self.reportTree.heading("orderSum", text="Number of Orders" )
        self.reportTree.heading("totAmt", text="TotalAmt")

        # CUSTOMER REP GENERATION
        self.reportTree.delete(*self.reportTree.get_children())

        listInc=1
        for row in self.dbResults:
            _values = [listInc, row[0], row[1], row[2], row[3], row[4], row[5]]
            self.reportTree.insert("", tk.END, value=_values)
            listInc+=1

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    reports = ReportsWindow(root)
    root.mainloop()
