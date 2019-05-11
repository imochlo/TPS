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

class PopupDashboard():
    def __init__(self, master, parentClass):
        self.master=master
        self.parentClass = parentClass

        self.pc=Services.Local(self.master)
        self.db=Services.Db()

    def genRmTable(self, tableInfo):
        self.top = Toplevel(self.master)
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        lblFrame=Frame(self.top)
        lblFrame.pack()
        lblFrame.pack(side=TOP, pady=[50,20], padx=100)

        lbl = Label(lblFrame, text="Are you sure you want to delete this item?")

        lbl = Label(lblFrame, text="Table No: " + str(tableInfo[1]))
        lbl.grid(row=0, sticky=W)
        lbl = Label(lblFrame, text="Size: " + str(tableInfo[2]))
        lbl.grid(row=1, sticky=W)
        lbl = Label(lblFrame, text="Checkout Preference: " + str(tableInfo[3]))
        lbl.grid(row=2, sticky=W)

        btnFrame = Frame(self.top)
        btnFrame.pack(side=TOP, pady=[20,50], padx=100)

        self.btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        self.btn.pack(side=RIGHT)
        self.btn = Button(btnFrame, text="Remove", command=lambda : self.genRemoveDone(tableInfo[0]))
        self.btn.pack(side=RIGHT, padx=10)

    def genRemoveDone(self, transNo):
        getTables="SELECT * FROM transactions WHERE transNo = " + str(transNo)
        pks = self.db.get(getTables)

        rmCustomer="DELETE FROM customer WHERE custNo = " + str(pks[0][1])
        rmInvoice="DELETE FROM invoice WHERE invoiceNo = " + str(pks[0][2])
        rmOrders="DELETE FROM foodOrders WHERE orderNo = " + str(transNo)
        rmTransaction="DELETE FROM transactions WHERE transNo = " + str(pks[0][0])

        self.db.set(rmCustomer)
        self.db.set(rmInvoice)
        self.db.set(rmOrders)
        self.db.set(rmTransaction)
        
        msgbox.showinfo("Item Removed", "Item Removed\n\n")
        self.parentClass.genTableTree()
        self.top.destroy()

    def genAddTable(self):
        self.top = Toplevel(self.master)
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        entryFrame = Frame(self.top)
        entryFrame.pack(side=TOP, pady=[50,20], padx=100)

        # Table No
        lbl=Label(entryFrame, text="Table No: ")
        lbl.grid(column=0, row=0, sticky=W)
        self.entryNo = Entry(entryFrame)
        self.entryNo.grid(column=1, row=0)
        self.entryNo.bind('<Button>', lambda event : self.entrySize.delete(0,END))

        # No. of Guests
        lbl=Label(entryFrame, text="No. of Guests")
        lbl.grid(column=0, row=1, sticky=W)

        self.entrySize = Entry(entryFrame)
        self.entrySize.grid(column=1, row=1, sticky=E)
        self.entrySize.bind('<Button>', lambda event : self.entrySize.delete(0,END))

        # Checkout Pref
        self.listboxCheckout = Listbox(entryFrame)
        self.listboxCheckout.grid(column=1, row=3)
        checkoutPref = ["Dine-In", "Take-Out", "Delivery"]
        for elem in checkoutPref:
            self.listboxCheckout.insert(END, elem)
        self.listboxCheckout.selection_set(0)

        # BUTTONS
        btnFrame = Frame(self.top)
        btnFrame.pack(side=TOP, pady=[20,50], padx=100)

        self.btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        self.btn.pack(side=RIGHT)

        self.btn = Button(btnFrame, text="Add", command=lambda : self.genAddDone())
        self.btn.pack(side=RIGHT, padx=10)

    def genAddDone(self):
        # Get Time and Date
        time=self.pc.getTimeNow()
        date=self.pc.getDateNow()
        
        # Get table info

        # Add Customer
        checkoutPref = self.listboxCheckout.get(self.listboxCheckout.curselection())
        addCustomer = "INSERT INTO customer(arrTime, checkoutPref) VALUES(\"%s\", \"%s\")" % (time, checkoutPref)
        self.db.set(addCustomer)
        custPK = int(self.db.get("SELECT max(custNo) FROM customer")[0][0])

        # Update Customer
        if len(self.entryNo.get()):
            updateTableNo = "UPDATE customer SET tableNo=%s WHERE custNo=%s" % (self.entrySize.get(), custPK)
            self.db.set(updateTableNo)
        if len(self.entrySize.get()):
            updateSize = "UPDATE customer SET partySize=%s WHERE custNo=%s" % (self.entrySize.get(), custPK)
            self.db.set(updateSize)

        # Add default invoice
        addInvoice = "INSERT INTO invoice(date, discount, ogPrice, totAmt) VALUES(%s, %s, %s, %s)" % (date, 0, 0, 0)
        self.db.set(addInvoice)
        invoicePK = int(self.db.get("SELECT max(invoiceNo) FROM invoice")[0][0])

        # Add transaction
        addTransaction = "INSERT INTO transactions(custNo, invoiceNo) VALUES(%s, %s)" % (custPK, invoicePK)
        self.db.set(addTransaction)

        transPK = int(self.db.get("SELECT max(transNo) FROM transactions")[0][0])
        self.parentClass.genTableTree()
        self.parentClass.genBillTree(transPK)
        self.top.destroy()

    def genBillOut(self, transNo):
        self.top = Toplevel(self.master)
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        # TABLE INFO
        lblFrame = Frame(self.top)
        lblFrame.pack(side=TOP, pady=50)
        custInfo = self.db.get("SELECT customer.tableNo, customer.checkoutPref FROM Transactions INNER JOIN customer ON transactions.custNo=customer.custNo WHERE transNo = %s" % transNo)
        billLabel = "For Table %s Billing" % custInfo[0][0] if (custInfo[0][0] != None) else "For %s Billing" % custInfo[0][1]

        lbl = Label(lblFrame, text= billLabel, font=30)
        lbl.pack()

        self.sumFrame = Frame(self.top)
        self.sumFrame.pack(expand=True, fill=BOTH, padx=50)

        self.sumTree = ttk.Treeview(self.sumFrame, column=("order","unit","qty","total"), show='headings')

        self.sumTree.column("order", width=200, anchor=W)
        self.sumTree.column("unit", width=100)
        self.sumTree.column("qty", width=100)
        self.sumTree.column("total", width=100, anchor=CENTER)

        self.sumTree.heading("order", text="Items")
        self.sumTree.heading("unit", text="Unit Price")
        self.sumTree.heading("qty", text="Qty")
        self.sumTree.heading("total", text="Total Price")

        self.sumTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.sumFrame, orient=VERTICAL, command=self.sumTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.sumTree.configure(yscrollcommand=self.scrollBar.set)


        billingSummary="SELECT menu.name, menu.price, foodOrders.qty FROM foodOrders INNER JOIN menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo WHERE transNo=%s" % transNo
        sumResults = self.db.get(billingSummary)

        self.ogPrice = 0
        self.sumTree.delete(*self.sumTree.get_children())
        for row in sumResults:
            name=row[0]
            unit=float(row[1]) if row[1] is not None else 0
            qty=int(row[2]) if row[2] is not None else 0
            total=unit*qty
            self.ogPrice+=total

            _values=[name, unit, qty, total]
            self.sumTree.insert("", tk.END, name, values=_values)

        self.sumTree.insert("", tk.END, "blank", values=["", "", "", ""])
        self.sumTree.insert("", tk.END, "total", values=["", "", "Total", self.ogPrice])

        outerFrame = Frame(self.top)
        outerFrame.pack(fill=X)
        entryFrame = Frame(outerFrame)
        entryFrame.pack(side=RIGHT, fill=X, pady=30, padx=50)
        
        self.totPrice=self.ogPrice
        lbl = Label(entryFrame, text="Total Price:")
        lbl.grid(row=0, column=0, sticky=W)
        self.lblTotal = Label(entryFrame, text=self.totPrice)
        self.lblTotal.grid(row=0, column=1, sticky=NSEW)

        lbl = Label(entryFrame, text="Discount Amount:")
        lbl.grid(row=1, column=0, sticky=W)
        self.entryDiscount = Entry(entryFrame, width=10, justify=CENTER)
        self.entryDiscount.grid(row=1, column=1)
        self.entryDiscount.insert(END, 0)
        self.entryDiscount.bind('<Button>', lambda event : self.entryDiscount.delete(0,END))
        self.entryDiscount.bind('<FocusIn>', lambda event : self.entryDiscount.delete(0,END))
        self.entryDiscount.bind('<Leave>', lambda event : self.recalculateTotal())
        self.entryDiscount.bind('<FocusOut>', lambda event : self.recalculateTotal())
        self.entryDiscount.bind('<Return>', lambda event : self.recalculateTotal())

        lbl = Label(entryFrame, text="%")
        lbl.grid(row=1, column=2)

        lbl = Label(entryFrame, text="Received Amount:")
        lbl.grid(row=2, column=0)
        self.entryRcv = Entry(entryFrame, width=10, justify=CENTER)
        self.entryRcv.grid(row=2, column=1)
        self.entryRcv.insert(END, 0)
        self.entryRcv.bind('<Button>', lambda event : self.entryRcv.delete(0,END))
        self.entryRcv.bind('<FocusIn>', lambda event : self.entryRcv.delete(0,END))
        self.entryRcv.bind('<Leave>', lambda event : self.recalculateChange())
        self.entryRcv.bind('<FocusOut>', lambda event : self.recalculateChange())
        self.entryRcv.bind('<Return>', lambda event : self.recalculateChange())

        lbl = Label(entryFrame, text="Change:")
        lbl.grid(row=3, column=0)
        self.lblChange = Label(entryFrame, text=self.totPrice)
        self.lblChange.grid(row=3, column=1, sticky=NSEW)

        btnFrame = Frame(self.top)
        btnFrame.pack(fill=X, pady=30, padx=50)
        
        process = Button(btnFrame, text="Proceed", width=50, height=3, font=30, command=lambda : self.processTransaction(transNo))
        process.pack(pady=5)
        cancel = Button(btnFrame, text="Cancel", width=50, height=3, font=30, command=self.top.destroy)
        cancel.pack()

    def processTransaction(self, transNo):
        discount = self.entryDiscount.get()
        ogPrice = self.ogPrice
        totAmt = self.totPrice
        rcvAmt = self.entryRcv.get()
        time=self.pc.getTimeNow()
        updateTransaction = "UPDATE transactions SET discount=%s, ogPrice=%s, totAmt=%s,rcvAmt=%s WHERE transNo=%s" % (discount, ogPrice, totAmt, rcvAmt, transNo)
        customerInfo = "SELECT custNo FROM transactions WHERE transNo=%s" % transNo
        custNo = int(self.db.get(customerInfo)[0][0])
        updateDeptTime = "UPDATE customer SET deptTime=\"%s\" WHERE custNo=%s" % (time, custNo)
        print(updateDeptTime)
        self.db.set(updateDeptTime)
        self.top.destroy()

    def recalculateTotal(self):
        discount = int(self.entryDiscount.get())
        self.totPrice = (100 - discount) * 0.01 * self.totPrice
        self.lblTotal.configure(text=self.totPrice)

    def recalculateChange(self):
        rcvAmt = int(self.entryRcv.get())
        change = (rcvAmt - self.totPrice) if rcvAmt > 0 else 0
        self.lblChange.configure(text=change)

class DashboardWindow():
    def __init__ (self, master):
        self.popup=PopupDashboard(master, self)

        self.tableSelectCol = "#7"
        self.tableRemoveCol = "#8"
        self.billMinusCol ="#4"
        self.billAddCol = "#6"
        self.billRmCol="#7"
        self.catAddCol="#3"
        self.activeBill=0

        self.master=master
        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Dashboard")

        self.init_catList()

        self.init_backBtn(master)

        self.frame2 = Frame(master)
        self.frame2.pack(side=TOP, fill=BOTH, expand=True)
        self.init_tableTree(self.frame2)
        self.genTableTree()

        self.frame3 = Frame(master)
        self.frame3.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_catBtn(self.frame3)

        self.frame4 = Frame(master)
        self.frame4.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_catTree(self.frame4)

        self.frame5 = Frame(master)
        self.frame5.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_billTree(self.frame5)

        self.frame6 = Frame(master)
        self.frame6.pack(side=LEFT, fill=BOTH, expand=True)
        self.init_billBtn(self.frame6)
        
        self.pc.setFullScreen(master)


    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2, command=self.master.destroy)
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_tableTree(self, frame):
        name_index=1
        price_index=3

        lblFrame=Frame(frame)
        lblFrame.pack(pady=[30,10], padx=20)
        lbl = Label(lblFrame, text="Open Tables", font=30)
        lbl.pack()

        self.tableFrame=Frame(frame)
        self.tableFrame.pack(side=TOP, expand=True, fill=BOTH, pady=[0,30], padx=20)

        self.tableTree = ttk.Treeview(self.tableFrame, column=("no", "tableNo", "partySize", "coPref", "qty", "totAmt", "select", "remove"), show='headings')
        ttk.Style().configure("Treeview", rowheight=50)

        self.tableTree.column("no", width=self.pc.percentScreenW(3), stretch=True, anchor=CENTER)
        self.tableTree.column("tableNo", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("partySize", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("coPref", width=self.pc.percentScreenW(20), stretch=True, anchor=CENTER)
        self.tableTree.column("qty", width=self.pc.percentScreenW(20), stretch=True, anchor=CENTER)
        self.tableTree.column("totAmt", width=self.pc.percentScreenW(20), stretch=True, anchor=CENTER)
        self.tableTree.column("select", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
        self.tableTree.column("remove", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
        
        self.tableTree.heading("no", text="")
        self.tableTree.heading("tableNo", text="Table No.")
        self.tableTree.heading("partySize", text="No. of Guests")
        self.tableTree.heading("coPref", text="Checkout Preference")
        self.tableTree.heading("qty", text="No. of Ordered Items")
        self.tableTree.heading("totAmt", text="Total Balance")
        self.tableTree.heading("select", text="")
        self.tableTree.heading("remove", text="")

        self.tableTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.tableScroll = ttk.Scrollbar(self.tableFrame, orient=VERTICAL, command=self.tableTree.yview)
        self.tableScroll.pack(side=RIGHT, fill=Y)
        self.tableTree.configure(yscrollcommand=self.tableScroll.set)

        self.tableTree.bind("<Button-1>", self.tableProcessClick)

    def init_catTree(self, frame):
        name_index=1
        price_index=3

        catTreeInnerFrame=Frame(frame)
        catTreeInnerFrame.pack(pady=[30,0], padx=20)
        lbl = Label(catTreeInnerFrame, text="Category Items", font=30)
        lbl.pack(pady=[0,10])

        self.foodFrame=Frame(catTreeInnerFrame)
        self.foodFrame.pack(expand=True, fill=BOTH, padx=20, pady=[0,30])

        self.catTree = ttk.Treeview(self.foodFrame, column=("name", "price", "add"), show='headings', selectmode="extended")
        
        self.catTree.column("name", width=self.pc.percentScreenW(15), stretch=True)
        self.catTree.column("price", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.catTree.column("add", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=False)
        
        self.catTree.heading("name", text="Name")
        self.catTree.heading("price", text="Price", anchor=CENTER)
        self.catTree.heading("add", text="", anchor=CENTER)
        self.catTree.grid(column=0, row=0, sticky=NSEW)

        self.catScroll = ttk.Scrollbar(self.foodFrame, orient=VERTICAL,  command=self.catTree.yview)
        self.catScroll.grid(column=1, row=0, sticky=NS)
        self.catTree.configure(yscrollcommand=self.catScroll.set)
        self.catTree.delete(*self.catTree.get_children())

        self.catTree.bind("<Button-1>", self.catProcessClick)

    def init_billTree(self, frame):
        name_index=1
        price_index=3

        billTreeInnerFrame=Frame(frame)
        billTreeInnerFrame.pack(pady=[30,0], padx=20)
        self.tableBill = Label(billTreeInnerFrame, text="Billing", font=30)
        self.tableBill.pack(pady=[0,10])

        self.billFrame=Frame(billTreeInnerFrame)
        self.billFrame.pack(expand=True, fill=BOTH, pady=[0,30], padx=20)

        self.billTree = ttk.Treeview(self.billFrame, column=("no", "name", "price", "minus", "qty", "add", "rm"), show='headings')
        
        self.billTree.column("no", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=False)
        self.billTree.column("name", width=self.pc.percentScreenW(15), stretch=True)
        self.billTree.column("price", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.billTree.column("minus", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=False)
        self.billTree.column("qty", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=True)
        self.billTree.column("add", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=True)
        self.billTree.column("rm", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=False)
        
        self.billTree.heading("no", text="")
        self.billTree.heading("name", text="Name")
        self.billTree.heading("price", text="Price")
        self.billTree.heading("minus", text="Minus")
        self.billTree.heading("qty", text="Qty")
        self.billTree.heading("add", text="Add")
        self.billTree.heading("rm", text="Remove")

        self.billTree.grid(column=0, row=0, sticky=NSEW)


        self.billScroll = ttk.Scrollbar(self.billFrame, orient=VERTICAL, command=self.billTree.yview)
        self.billScroll.grid(column=1, row=0, sticky=NS)
        self.billTree.configure(yscrollcommand=self.billScroll.set)

        self.billTree.bind("<Button-1>", self.billProcessClick)

    def init_billBtn(self, frame):
        billBtnOuterFrame=Frame(frame)
        billBtnOuterFrame.pack(side=LEFT, padx=[0,40], pady=[30,10])
        self.billoutFrame=Frame(billBtnOuterFrame)
        self.billoutFrame.pack()
        self.billBtn=Button(self.billoutFrame, text="Bill Out", height=3, width=7, background="green", foreground="white", font='bold', command=lambda : self.billout())
        self.billBtn.pack(side=TOP, pady=10)
        self.cancelBtn=Button(self.billoutFrame, text="Cancel", height=3, width=7, background="red", foreground="white", font='bold', command=lambda : self.cancelBill())
        self.cancelBtn.pack(side=TOP, pady=10)

    def init_catBtn(self, frame):

        billBtnOuterFrame=Frame(frame)
        billBtnOuterFrame.pack(side=LEFT, padx=[40,0], pady=[30,0])
        billBtnInnerFrame= Frame(billBtnOuterFrame)
        billBtnInnerFrame.pack()
        lbl = Label(billBtnInnerFrame, text="Category List", font=30)
        lbl.pack(pady=[0,10])

        self.catBtnFrame=Frame(billBtnInnerFrame)
        self.catBtnFrame.pack(padx=30)
        row_num=0

        for i in range(len(self.catList)):
            elem = self.catList[i]
            self.btn = Button(self.catBtnFrame, text=self.catList[i], width=10, height=2, command=lambda cat=elem:self.genCatTree(cat))
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

        self.tableResults = self.db.get("SELECT transactions.transNo, customer.tableNo, customer.partySize, customer.checkoutPref, sum(foodOrders.qty), invoice.ogPrice FROM invoice INNER JOIN transactions ON invoice.invoiceNo=transactions.transNo LEFT JOIN foodOrders ON transactions.transNo=foodOrders.orderNo INNER JOIN customer ON transactions.custNo=customer.custNo WHERE invoice.rcvAmt IS NULL GROUP BY foodOrders.orderNo ORDER BY customer.arrTime ASC")

        self.tableInc=0
        self.tableTree.insert("", tk.END, self.tableInc, values=("", "", "", "", "", "", "Add Table", "Add Table"))

        for row in self.tableResults:
            self.tableInc+=1
            _values=[self.tableInc, row[1], row[2], row[3], row[4], row[5], "Select", "Remove"]
            self.tableTree.insert("", tk.END, self.tableInc, values=_values)

        self.tableInc+=1
        self.tableTree.insert("", tk.END, self.tableInc, values=("", "", "", "", "", "", "Add Table", "Add Table"))
        ttk.Style().configure("Treeview", rowheight=30)

    def genCatTree(self, cat):
        name_index=1
        price_index=3

        self.catTree.delete(*self.catTree.get_children())
        self.catResults=self.db.get("SELECT * FROM menu WHERE category = \"%s\" " % cat)

        for row in self.catResults:
            _values=[row[name_index], row[price_index], "add"]
            self.catTree.insert("", tk.END, row[0], values=_values)

    def tableProcessClick(self, event):
        item = self.tableTree.identify('item', event.x, event.y)
        row = self.tableTree.identify_row(event.y)
        col = self.tableTree.identify_column(event.x)
        
        if row.isnumeric():
            elem=int(row)-1
            if (col == self.tableSelectCol):
                self.genBillTree(self.tableResults[elem][0])
            elif (col == self.tableRemoveCol):
                self.popup.genRmTable(self.tableResults[elem])
        elif (col == self.tableSelectCol):
            self.popup.genAddTable()

    def billProcessClick(self, event):
        item = self.billTree.identify('item', event.x, event.y)
        row = self.billTree.identify_row(event.y)
        col = self.billTree.identify_column(event.x)
        
        if row.isnumeric():
            elem=int(row)-1
            orderNo = self.activeBill
            menuNo=self.billResults[elem][4] 
            qty=int(self.billResults[elem][3])

            if (col == self.billAddCol):
                qty+=1
            elif (col == self.billMinusCol):
                qty-=1

            updateBilling = "UPDATE foodOrders SET qty=%s WHERE orderNo=%s AND menuNo=%s" % (qty, orderNo, menuNo)

            if (col == self.billRmCol or qty<=0):
                updateBilling = "DELETE FROM foodOrders WHERE orderNo=%s AND menuNo=%s" % (orderNo, menuNo)

            self.db.set(updateBilling)
            self.updateBillTotal(self.activeBill)
            self.genBillTree(self.activeBill)

    def updateBillTotal(self, transNo):
        orderSummary="SELECT menu.price, foodOrders.qty, transactions.invoiceNo FROM transactions LEFT JOIN foodOrders ON transactions.transNo=foodOrders.orderNo LEFT JOIN menu ON foodOrders.menuNo=menu.menuNo WHERE transNo=%s" % transNo
        orderResults = self.db.get(orderSummary)

        ogPrice = 0
        for row in orderResults:
            unit=float(row[0]) if row[1] is not None else 0
            qty=int(row[1]) if row[1] is not None else 0
            ogPrice+=unit*qty

        updateTotal="UPDATE invoice SET ogPrice=%s WHERE invoiceNo=%s" % (ogPrice, orderResults[0][2])
        self.db.set(updateTotal)
        self.genTableTree()

    def catProcessClick(self, event):
        item = self.catTree.identify('item', event.x, event.y)
        row = self.catTree.identify_row(event.y)
        col = self.catTree.identify_column(event.x)

        if (col == self.catAddCol and self.activeBill>0):
            updateBilling = "INSERT INTO foodOrders(orderNo, menuNo, qty) VALUES(%s, %s, %s)" % (self.activeBill, row, 1)

            for elem in self.billResults:
                if (row == str(elem[4])):
                    qty=elem[3]+1
                    updateBilling = "UPDATE foodOrders SET qty=%s WHERE orderNo=%s AND menuNo=%s" % (qty, self.activeBill, row)
            
            self.db.set(updateBilling)
        elif col == self.catAddCol and self.activeBill == 0:
            msgbox.showerror("Error", "No table selected")

        self.updateBillTotal(self.activeBill)
        self.genBillTree(self.activeBill)

    def genBillTree(self, transNo):
        self.activeBill = transNo            

        #Fix Label
        custInfo = self.db.get("SELECT customer.tableNo, customer.checkoutPref FROM Transactions INNER JOIN customer ON transactions.custNo=customer.custNo WHERE transNo = %s" % transNo)
        billLabel = "For Table %s Billing" % custInfo[0][0] if (custInfo[0][0] != None) else "For %s Billing" % custInfo[0][1]
        self.tableBill.configure(text=billLabel)

        #Get Billing Info
        self.billTree.delete(*self.billTree.get_children())
        self.billResults = self.db.get("SELECT foodOrders.orderNo, menu.name, menu.price, foodOrders.qty, foodOrders.menuNo FROM foodOrders LEFT JOIN menu ON foodOrders.menuNo=menu.menuNo WHERE foodOrders.orderNo=%s" % self.activeBill)

        self.billInc=1
        for row in self.billResults:
            _values=[self.billInc, row[1], row[2], "-", row[3], "+", "Remove"]
            self.billTree.insert("", tk.END, self.billInc, values=_values)
            self.billInc+=1
    
    def cancelBill(self):
        self.billTree.delete(*self.billTree.get_children())
        self.activeBill = 0
        self.tableBill.configure(text="Billing")

    def billout(self):
        if (self.activeBill > 0):
            self.popup.genBillOut(self.activeBill)
        else:
            msgbox.showerror("Error", "No Bill Selected")

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    dashboard = DashboardWindow(root)
    root.mainloop()
