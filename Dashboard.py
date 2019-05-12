#/usr/bin/python
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

        self.master = master
        self.parentClass = parentClass

        self.pc = Services.Local(self.master)
        self.db = Services.Db()

    def genRmTable(self, tableInfo):

        self.top = Toplevel(self.master)

        topFrame = Frame(self.top)
        topFrame.pack(expand=True, pady=50, padx=100)

        self.top.title("Removing Table")
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        lblFrame=Frame(topFrame)
        lblFrame.pack()

        lbl = Label(lblFrame, text="Are you sure you want to delete this item?", justify=LEFT)

        lbl = Label(lblFrame, text="Table No: " + str(tableInfo[1]), justify=LEFT)
        lbl.grid(row=0, sticky=W)
        lbl = Label(lblFrame, text="Size: " + str(tableInfo[2]), justify=LEFT)
        lbl.grid(row=1, sticky=W)
        lbl = Label(lblFrame, text="Checkout Preference: " + str(tableInfo[3]), justify=LEFT)
        lbl.grid(row=2, sticky=W)

        btnFrame = Frame(topFrame)
        btnFrame.pack(side=RIGHT, pady=[20,0])

        btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        btn.pack(side=RIGHT)
        btn = Button(btnFrame, text="Remove", command=lambda : self.genRemoveDone(tableInfo[0]))
        btn.pack(side=RIGHT, padx=[0,10])

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

        self.parentClass.genOpenTablesTree()
        self.top.destroy()

    def genAddTable(self):

        self.top = Toplevel(self.master)
        self.top.title("Add Table")
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        mainFrame = Frame(self.top)
        mainFrame.pack(expand=True, padx=100, pady=100)

        entryFrame = Frame(mainFrame)
        entryFrame.pack()

        # TABLE NO
        lbl=Label(entryFrame, text="Table No:")
        lbl.grid(column=0, row=0, sticky=W)
        self.entryNo = Entry(entryFrame)
        self.entryNo.grid(column=1, row=0)
        self.entryNo.bind('<Button>', lambda event : self.entrySize.delete(0,END))

        # NO. OF GUESTS
        lbl=Label(entryFrame, text="No. of Guests:")
        lbl.grid(column=0, row=1, sticky=W)

        self.entrySize = Entry(entryFrame)
        self.entrySize.grid(column=1, row=1, sticky=E)
        self.entrySize.bind('<Button>', lambda event : self.entrySize.delete(0,END))

        # CHECKOUT PREF
        lbl=Label(entryFrame, text="Checkout Preference:")
        lbl.grid(column=0, row=2, sticky=NW)

        self.listboxCheckout = Listbox(entryFrame)
        self.listboxCheckout.grid(column=1, row=2)
        self.listboxCheckout.insert(0, "Dine-In")
        self.listboxCheckout.insert(1, "Take-Out")
        self.listboxCheckout.insert(2, "Delivery")
        self.listboxCheckout.selection_set(0)

        # BUTTONS
        btnFrame = Frame(mainFrame)
        btnFrame.pack(side=RIGHT, pady=[30,0])

        self.btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        self.btn.pack(side=RIGHT)

        self.btn = Button(btnFrame, text="Add", command=lambda : self.genAddDone())
        self.btn.pack(side=RIGHT, padx=10)

    def genAddDone(self):

        # GET TIME AND DATE
        time=self.pc.getTimeNow()
        date=self.pc.getDateNow()
        
        # ADD CUSTOMER
        checkoutPref = self.listboxCheckout.get(ANCHOR) if len(self.listboxCheckout.get(ANCHOR)) > 0 else "Dine-In"
        addCustomer = "INSERT INTO customer(arrTime, checkoutPref) VALUES(\"%s\", \"%s\")" % (time, checkoutPref)
        self.db.set(addCustomer)
        custPK = int(self.db.get("SELECT max(custNo) FROM customer")[0][0])

        # UPDATE CUSTOMER
        if len(self.entryNo.get()) > 0:
            updateTableNo = "UPDATE customer SET tableNo=%s WHERE custNo=%s" % (self.entryNo.get(), custPK)
            self.db.set(updateTableNo)
        if len(self.entrySize.get()) > 0:
            updateSize = "UPDATE customer SET partySize=%s WHERE custNo=%s" % (self.entrySize.get(), custPK)
            self.db.set(updateSize)

        # ADD INVOICE
        addInvoice = "INSERT INTO invoice(date, discount, ogPrice, totAmt) VALUES(\"%s\", %s, %s, %s)" % (date, 0, 0, 0)
        self.db.set(addInvoice)
        invoicePK = int(self.db.get("SELECT max(invoiceNo) FROM invoice")[0][0])

        # ADD TRANSACTION
        addTransaction = "INSERT INTO transactions(custNo, invoiceNo) VALUES(%s, %s)" % (custPK, invoicePK)
        self.db.set(addTransaction)

        transPK = int(self.db.get("SELECT max(transNo) FROM transactions")[0][0])
        self.parentClass.genOpenTablesTree()
        self.parentClass.genTableOrders(transPK)
        self.top.destroy()

    def genBillOut(self, transNo):

        self.top = Toplevel(self.master)
        self.top.title("Billing Out")
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        outerFrame = Frame(self.top)
        outerFrame.pack(expand=True, padx=100, pady=100)

        # LABEL SET UP
        lblFrame = Frame(outerFrame)
        lblFrame.pack(side=TOP, fill=X)
        custInfo = self.db.get("SELECT customer.tableNo, customer.checkoutPref FROM Transactions INNER JOIN customer ON transactions.custNo=customer.custNo WHERE transNo = %s" % transNo)
        billLabel = "For Table %s Order" % custInfo[0][0] if (custInfo[0][0] != None) else "For %s Order" % custInfo[0][1]

        lbl = Label(lblFrame, text= billLabel, font=30)
        lbl.pack()

        sumFrame = Frame(outerFrame)
        sumFrame.pack(fill=X)

        # TREE SUMMARY SET UP
        sumTree = ttk.Treeview(sumFrame, column=("order","unit","qty","total"), show='headings')
        ttk.Style().configure("Treeview")

        sumTree.column("order", width=200, anchor=W)
        sumTree.column("unit", width=100)
        sumTree.column("qty", width=100)
        sumTree.column("total", width=100, anchor=CENTER)

        sumTree.heading("order", text="Items")
        sumTree.heading("unit", text="Unit Price")
        sumTree.heading("qty", text="Qty")
        sumTree.heading("total", text="Total Price")

        sumTree.pack(side=LEFT)

        scrollbar = ttk.Scrollbar(sumFrame, orient=VERTICAL, command=sumTree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        sumTree.configure(yscrollcommand=scrollbar.set)

        # PRINT ORDER SUMMARY  
        orderSummary="SELECT menu.name, menu.price, foodOrders.qty FROM foodOrders INNER JOIN menu ON foodOrders.menuNo=menu.menuNo LEFT JOIN transactions ON foodOrders.orderNo=transactions.transNo WHERE transNo=%s" % transNo
        orderSumResults = self.db.get(orderSummary)

        sumTree.delete(*sumTree.get_children())

        for row in orderSumResults:
            name=row[0]
            unit=float(row[1]) if row[1] is not None else 0
            qty=int(row[2]) if row[2] is not None else 0
            total=unit*qty

            _values=[name, unit, qty, total]
            sumTree.insert("", tk.END, name, values=_values)

        # PRINT BILL SUMMARY
        self.ogPrice = int(self.db.get("SELECT ogprice FROM invoice INNER JOIN transactions ON invoice.invoiceNo = transactions.invoiceNo WHERE transactions.transNo = %s" % transNo)[0][0])
        outerEntryFrame = Frame(outerFrame)
        outerEntryFrame.pack(fill=X)

        innerEntryFrame = Frame(outerEntryFrame)
        innerEntryFrame.pack(side=RIGHT, pady=[30,0])
        
        # TOTAL PRICE
        self.totPrice=round(self.ogPrice,2)
        lbl = Label(innerEntryFrame, text="Total Price:")
        lbl.grid(row=0, column=0, sticky=W)
        self.lblTotal = Label(innerEntryFrame, text=self.totPrice)
        self.lblTotal.grid(row=0, column=1, sticky=NSEW)

        # DISCOUNT AMT
        lbl = Label(innerEntryFrame, text="Discount Amount:")
        lbl.grid(row=1, column=0, sticky=W)

        self.entryDiscount = Entry(innerEntryFrame, width=10, justify=CENTER)
        self.entryDiscount.grid(row=1, column=1)
        self.entryDiscount.insert(END, 0)
        self.entryDiscount.bind('<Button>', lambda event : self.entryDiscount.delete(0,END))
        self.entryDiscount.bind('<FocusIn>', lambda event : self.entryDiscount.delete(0,END))
        self.entryDiscount.bind('<FocusOut>', lambda event : self.recalculateTotal())
        self.entryDiscount.bind('<Return>', lambda event : self.recalculateTotal())

        lbl = Label(innerEntryFrame, text="%")
        lbl.grid(row=1, column=2)

        # RECEIVED AMT
        lbl = Label(innerEntryFrame, text="Received Amount:")
        lbl.grid(row=2, column=0)

        self.entryRcv = Entry(innerEntryFrame, width=10, justify=CENTER)
        self.entryRcv.grid(row=2, column=1)
        self.entryRcv.insert(END, 0)
        self.entryRcv.bind('<Button>', lambda event : self.entryRcv.delete(0,END))
        self.entryRcv.bind('<FocusIn>', lambda event : self.entryRcv.delete(0,END))
        self.entryRcv.bind('<FocusOut>', lambda event : self.recalculateChange())
        self.entryRcv.bind('<Return>', lambda event : self.recalculateChange())

        # CHANGE
        lbl = Label(innerEntryFrame, text="Change:")
        lbl.grid(row=3, column=0)
        self.lblChange = Label(innerEntryFrame, text=self.totPrice)
        self.lblChange.grid(row=3, column=1, sticky=NSEW)
        self.lblChange.configure(text=0)

        btnFrame = Frame(outerFrame)
        btnFrame.pack(fill=X, pady=[30,0])
        
        btnProcess = Button(btnFrame, text="Proceed", height=2, font=30, command=lambda : self.processTransaction(transNo))
        btnProcess.pack(fill=X, pady=3)
        btnCancel = Button(btnFrame, text="Cancel", height=2, font=30, command=self.top.destroy)
        btnCancel.pack(fill=X)

    def processTransaction(self, transNo):

        discount = self.entryDiscount.get()
        ogPrice = self.ogPrice
        totAmt = self.totPrice
        rcvAmt = self.entryRcv.get()
        time=self.pc.getTimeNow()

        transactionInfo = self.db.get("SELECT custNo, invoiceNo FROM transactions WHERE transNo=%s" % transNo)
        custNo = int(transactionInfo[0][0])
        invoiceNo = int(transactionInfo[0][1])

        updateTableInvoice = "UPDATE invoice SET discount=%s, ogPrice=%s, totAmt=%s, rcvAmt=%s WHERE invoiceNo=%s" % (discount, ogPrice, totAmt, rcvAmt, invoiceNo)
        self.db.set(updateTableInvoice)

        updateTableDeptTime = "UPDATE customer SET deptTime=\"%s\" WHERE custNo=%s" % (time, custNo)
        self.db.set(updateTableDeptTime)

        self.parentClass.genOpenTablesTree()
        self.parentClass.activeTable=0
        self.parentClass.tableOrdersTree.delete(*self.parentClass.tableOrdersTree.get_children())
        self.parentClass.lblTable.configure(text="For Orders")
        self.top.destroy()

    def recalculateTotal(self):

        discount = self.entryDiscount.get()
        if (discount.isnumeric() and int(discount) < 100):
            self.totPrice = round(((100 - int(discount)) * 0.01 * self.ogPrice),2)
            self.lblTotal.configure(text=self.totPrice)
        else:
            self.entryDiscount.delete(0,END)
            self.entryDiscount.insert(0,0)

    def recalculateChange(self):

        rcvAmt = int(self.entryRcv.get()) if self.entryRcv.get().isnumeric() else 0
        change = round((rcvAmt - self.totPrice)) if rcvAmt > 0 else 0
        self.lblChange.configure(text=change)

        self.entryRcv.delete(0,END)
        self.entryRcv.insert(0,rcvAmt)

class DashboardWindow():
    def __init__ (self, master):

        self.popup=PopupDashboard(master, self)
        self.activeTable=0

        self.master=master
        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Dashboard")

        self.init_catList()

        self.init_backBtn(master)

        upperBodyFrame = Frame(master)
        upperBodyFrame.pack(expand=True, fill=BOTH, padx=50, pady=15)
        self.init_openTablesTree(upperBodyFrame)
        self.genOpenTablesTree()

        lowerBodyFrame = Frame(master)
        lowerBodyFrame.pack(expand=True, fill=Y, padx=50, pady=15)

        outerCatBtnFrame = Frame(lowerBodyFrame)
        outerCatBtnFrame.pack(side=LEFT, fill=Y)
        self.init_catBtn(outerCatBtnFrame)

        self.outerCatTreeFrame = Frame(lowerBodyFrame)
        self.outerCatTreeFrame.pack(side=LEFT)
        self.init_catTree(self.outerCatTreeFrame)

        outerTableOrderTreeFrame = Frame(lowerBodyFrame)
        outerTableOrderTreeFrame.pack(side=LEFT)
        self.init_tableOrdersTree(outerTableOrderTreeFrame)

        outerTableOrderBtnFrame = Frame(lowerBodyFrame)
        outerTableOrderBtnFrame.pack(side=LEFT, fill=Y)
        self.init_tableBillOutBtn(outerTableOrderBtnFrame)
        
        self.pc.setFullScreen(master)

    def init_catList(self):

        dbResults = self.db.get("SELECT DISTINCT category FROM menu")
        self.catList = []

        for elem in dbResults:
            self.catList.append(elem[0])

    def init_backBtn(self, frame):

        btnBack = Button(frame, text="Back to main window", height=2, command=lambda : self.master.destroy())
        btnBack.pack(side=TOP, fill=BOTH)

    def init_openTablesTree(self, frame):

        lblFrame=Frame(frame)
        lblFrame.pack()
        lbl = Label(lblFrame, text="Open Tables", font=30)
        lbl.pack()

        openTableTreeFrame=Frame(frame)
        openTableTreeFrame.pack(side=TOP, expand=True, fill=BOTH)

        self.tableTree = ttk.Treeview(openTableTreeFrame, column=("no", "tableNo", "partySize", "coPref", "qty", "totAmt", "select", "remove"), show='headings')
        ttk.Style().configure("Treeview", rowheight=50)

        self.tableTree.column("no", width=self.pc.percentScreenW(3), stretch=True, anchor=CENTER)
        self.tableTree.column("tableNo", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("partySize", width=self.pc.percentScreenW(5), stretch=True, anchor=CENTER)
        self.tableTree.column("coPref", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
        self.tableTree.column("qty", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
        self.tableTree.column("totAmt", width=self.pc.percentScreenW(10), stretch=True, anchor=CENTER)
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

        openTablesScroll = ttk.Scrollbar(openTableTreeFrame, orient=VERTICAL, command=self.tableTree.yview)
        openTablesScroll.pack(side=RIGHT, fill=Y)
        self.tableTree.configure(yscrollcommand=openTablesScroll.set)

        self.tableTree.bind("<Button-1>", self.tableProcessClick)

    def init_catBtn(self, frame):

        lbl = Label(frame, text="Category List", font=30)
        lbl.pack(pady=[0,10])

        btnFrame=Frame(frame)
        btnFrame.pack(expand=True)

        row_num=0
        for i in range(len(self.catList)):
            elem = self.catList[i]
            self.btn = Button(btnFrame, text=self.catList[i], width=10, height=2, command=lambda category=elem : self.genCatTree(category))
            if (i%2==0):
                self.btn.grid(row=row_num, column=0, padx=5, pady=5)
            else:
                self.btn.grid(row=row_num, column=1, padx=5, pady=5)
                row_num+=1

    def init_catTree(self, frame):

        lbl = Label(frame, text="Category Items", font=30)
        lbl.pack(pady=[0,15])

        self.foodFrame=Frame(frame)
        self.foodFrame.pack(expand=True, padx=20)

        self.catTree = ttk.Treeview(self.foodFrame, column=("name", "price", "add"), show='headings', selectmode="extended")
        ttk.Style().configure("Treeview", rowheight=50)
        
        self.catTree.column("name", width=self.pc.percentScreenW(20), stretch=True)
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

    def init_tableOrdersTree(self, frame):

        self.lblTable = Label(frame, text="Table Orders", font=30)
        self.lblTable.pack(pady=[0,15])

        tableOrdersTreeFrame=Frame(frame)
        tableOrdersTreeFrame.pack(expand=True, padx=20)

        self.tableOrdersTree = ttk.Treeview(tableOrdersTreeFrame, column=("no", "name", "price", "minus", "qty", "add", "rm"), show='headings')
        ttk.Style().configure("Treeview", rowheight=50)
        
        self.tableOrdersTree.column("no", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=False)
        self.tableOrdersTree.column("name", width=self.pc.percentScreenW(15), stretch=True)
        self.tableOrdersTree.column("price", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=True)
        self.tableOrdersTree.column("minus", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=False)
        self.tableOrdersTree.column("qty", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=True)
        self.tableOrdersTree.column("add", width=self.pc.percentScreenW(3), anchor=CENTER, stretch=True)
        self.tableOrdersTree.column("rm", width=self.pc.percentScreenW(5), anchor=CENTER, stretch=False)
        
        self.tableOrdersTree.heading("no", text="")
        self.tableOrdersTree.heading("name", text="Name")
        self.tableOrdersTree.heading("price", text="Price")
        self.tableOrdersTree.heading("minus", text="Minus")
        self.tableOrdersTree.heading("qty", text="Qty")
        self.tableOrdersTree.heading("add", text="Add")
        self.tableOrdersTree.heading("rm", text="Remove")

        self.tableOrdersTree.grid(column=0, row=0, sticky=NSEW)


        self.billScroll = ttk.Scrollbar(tableOrdersTreeFrame, orient=VERTICAL, command=self.tableOrdersTree.yview)
        self.billScroll.grid(column=1, row=0, sticky=NS)
        self.tableOrdersTree.configure(yscrollcommand=self.billScroll.set)

        self.tableOrdersTree.bind("<Button-1>", self.billProcessClick)

    def init_tableBillOutBtn(self, frame):

        btnFrame=Frame(frame)
        btnFrame.pack(expand=True)

        self.billBtn=Button(btnFrame, text="Bill Out", height=3, width=7, background="green", foreground="white", font='bold', command=lambda : self.billout())
        self.billBtn.pack(pady=10)
        self.cancelBtn=Button(btnFrame, text="Cancel", height=3, width=7, background="red", foreground="white", font='bold', command=lambda : self.cancelBill())
        self.cancelBtn.pack(pady=10)

    def genOpenTablesTree(self):
        
        self.tableTree.delete(*self.tableTree.get_children())

        self.tableResults = self.db.get("SELECT transactions.transNo, customer.tableNo, customer.partySize, customer.checkoutPref, sum(qty), invoice.totAmt FROM transactions LEFT JOIN invoice ON transactions.invoiceNo=invoice.invoiceNo LEFT JOIN foodOrders ON foodOrders.orderNo=transactions.transNo LEFT JOIN customer on transactions.custNo=customer.custNo WHERE invoice.rcvAmt IS NULL GROUP BY transactions.transNo ORDER BY customer.arrTime DESC")

        self.tableInc=1
        self.tableTree.insert("", tk.END, 0, values=("", "", "", "", "", "", "Add Table", "Add Table"))

        for row in self.tableResults:
            qty = 0 if row[4] == None else row[4]

            _values=[self.tableInc, row[1], row[2], row[3], qty, row[5], "Select", "Remove"]
            self.tableTree.insert("", tk.END, self.tableInc, values=_values)
            self.tableInc+=1

        self.tableTree.insert("", tk.END, self.tableInc, values=("", "", "", "", "", "", "Add Table", "Add Table"))

    def genCatTree(self, cat):


        self.catTree.delete(*self.catTree.get_children())
        self.catResults=self.db.get("SELECT menuNo, name, price FROM menu WHERE category = \"%s\" " % cat)

        for row in self.catResults:
            _values=[row[1], row[2], "add"]
            self.catTree.insert("", tk.END, row[0], values=_values)

    def tableProcessClick(self, event):

        item = self.tableTree.identify('item', event.x, event.y)
        row = self.tableTree.identify_row(event.y)
        col = self.tableTree.identify_column(event.x)

        selectCol = "#7"
        removeCol = "#8"
        
        if row.isnumeric():
            if int(row) > 0 and int(row) <= len(self.tableResults):
                elem=int(row)-1
                if (col == selectCol):
                    self.genTableOrders(self.tableResults[elem][0])
                elif (col == removeCol):
                    self.popup.genRmTable(self.tableResults[elem])
            elif (col == selectCol or col == removeCol):
                self.popup.genAddTable()

    def billProcessClick(self, event):

        item = self.tableOrdersTree.identify('item', event.x, event.y)
        row = self.tableOrdersTree.identify_row(event.y)
        col = self.tableOrdersTree.identify_column(event.x)
        minusCol ="#4"
        addCol = "#6"
        removeCol="#7"
        
        if row.isnumeric():
            elem=int(row)-1
            orderNo = self.activeTable
            menuNo=self.tableOrderResults[elem][4] 
            qty=int(self.tableOrderResults[elem][3])

            if (col == addCol):
                qty+=1
            elif (col == minusCol):
                qty-=1

            updateBilling = "UPDATE foodOrders SET qty=%s WHERE orderNo=%s AND menuNo=%s" % (qty, orderNo, menuNo)

            if (col == removeCol or qty<=0):
                updateBilling = "DELETE FROM foodOrders WHERE orderNo=%s AND menuNo=%s" % (orderNo, menuNo)

            self.db.set(updateBilling)
            self.updateTableOrderInvoice(self.activeTable)
            self.genTableOrders(self.activeTable)

    def updateTableOrderInvoice(self, transNo):

        orderSummary="SELECT menu.price, foodOrders.qty, transactions.invoiceNo FROM transactions LEFT JOIN foodOrders ON transactions.transNo=foodOrders.orderNo LEFT JOIN menu ON foodOrders.menuNo=menu.menuNo WHERE transNo=%s" % transNo
        orderResults = self.db.get(orderSummary)

        ogPrice = 0
        for row in orderResults:
            unit=float(row[0]) if row[1] is not None else 0
            qty=int(row[1]) if row[1] is not None else 0
            ogPrice+=unit*qty

        updateTotal="UPDATE invoice SET ogPrice=%s, totAmt=%s WHERE invoiceNo=%s" % (ogPrice, ogPrice, orderResults[0][2])
        self.db.set(updateTotal)
        self.genOpenTablesTree()

    def catProcessClick(self, event):

        item = self.catTree.identify('item', event.x, event.y)
        row = self.catTree.identify_row(event.y)
        col = self.catTree.identify_column(event.x)
        addCol="#3"

        if (col == addCol and self.activeTable>0):
            updateTableOrders = "INSERT INTO foodOrders(orderNo, menuNo, qty) VALUES(%s, %s, %s)" % (self.activeTable, row, 1)

            for order in self.tableOrderResults:
                if (row == str(order[4])):
                    qty=order[3]+1
                    updateTableOrders = "UPDATE foodOrders SET qty=%s WHERE orderNo=%s AND menuNo=%s" % (qty, self.activeTable, row)
            
            self.db.set(updateTableOrders)
        elif col == addCol and self.activeTable == 0:
            msgbox.showerror("Error", "No table selected")

        self.updateTableOrderInvoice(self.activeTable)
        self.genTableOrders(self.activeTable)

    def genTableOrders(self, transNo):

        self.activeTable = transNo            

        # UPDATE TABLE LABEL
        custInfo = self.db.get("SELECT customer.tableNo, customer.checkoutPref FROM Transactions INNER JOIN customer ON transactions.custNo=customer.custNo WHERE transNo = %s" % transNo)
        billLabel = "For Table %s Orders" % custInfo[0][0] if (custInfo[0][0] != None) else "For %s Orders" % custInfo[0][1]
        self.lblTable.configure(text=billLabel)

        # GET BILLING INFO
        self.tableOrdersTree.delete(*self.tableOrdersTree.get_children())
        self.tableOrderResults = self.db.get("SELECT foodOrders.orderNo, menu.name, menu.price, foodOrders.qty, foodOrders.menuNo FROM foodOrders LEFT JOIN menu ON foodOrders.menuNo=menu.menuNo WHERE foodOrders.orderNo=%s" % self.activeTable)

        self.billInc=1
        for row in self.tableOrderResults:
            _values=[self.billInc, row[1], row[2], "-", row[3], "+", "Remove"]
            self.tableOrdersTree.insert("", tk.END, self.billInc, values=_values)
            self.billInc+=1
    
    def cancelBill(self):

        self.tableOrdersTree.delete(*self.tableOrdersTree.get_children())
        self.activeTable = 0
        self.lblTable.configure(text="Table Orders")

    def billout(self):

        if (self.activeTable > 0):
            self.popup.genBillOut(self.activeTable)
        else:
            msgbox.showerror("Error", "No Table Selected")

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    dashboard = DashboardWindow(root)
    root.mainloop()
