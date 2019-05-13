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
no_index=0
name_index=1
cat_index=2
price_index=3
image_index=4

class PopupMenu():
    def __init__ (self, master, parentClass):
        self.master=master
        self.parentClass = parentClass

        self.pc = Services.Local(self.master)
        self.db = Services.Db()

    def popWindow(self, process, menuItem):
        self.top=Toplevel(self.master)
        self.top.title(process)
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        self.process=process

        if menuItem != None:
            self.menuNo=menuItem[0]
            self.menuCat=menuItem[1]
            self.menuName=menuItem[2]
            self.menuPrice=menuItem[3]

        frame = Frame(self.top)
        frame.pack(padx=100, pady=50, expand=True)

        if (process == "Remove Item"):
            self.genRemoveWindow(frame)
        else:
            self.genTemplateWindow(frame)

    def genRemoveWindow(self, frame):
        lblFrame = Frame(frame)
        lblFrame.pack()

        lbl = Label(lblFrame, text="Are you sure you want to delete this item?", justify=LEFT)
        lbl.pack(side=TOP, pady=[0,20])

        lbl = Label(lblFrame, text="Name: " + self.menuName, justify=LEFT)
        lbl.pack(side=TOP, anchor=W)
        lbl = Label(lblFrame, text="Category: " + self.menuCat, justify=LEFT)
        lbl.pack(side=TOP, anchor=W)
        lbl = Label(lblFrame, text="Price: " + str( self.menuPrice), justify=LEFT)
        lbl.pack(side=TOP, anchor=W)

        btnFrame = Frame(frame)
        btnFrame.pack(anchor=E, side=TOP, pady=[20,0])

        btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        btn.pack(side=RIGHT)
        btn = Button(btnFrame, text="Remove", command=lambda : self.genRemoveDone())
        btn.pack(side=RIGHT, padx=10)

    def genTemplateWindow(self, frame):
        catList = self.db.get("SELECT DISTINCT category FROM menu")

        entryFrame = Frame(frame)
        entryFrame.pack(anchor=W,expand=True, fill=BOTH)

        # NAME ENTRY
        lbl=Label(entryFrame, text="Name: ", justify=LEFT)
        lbl.grid(column=0, row=0, sticky=W)
        self.entryName = Entry(entryFrame)
        self.entryName.grid(column=1, row=0)
        if (self.process == "Edit Item"):
            self.entryName.insert(0, self.menuName)

        # CATEGORY ENTRY
        lbl=Label(entryFrame, text="Category: ")
        lbl.grid(column=0, row=2, sticky=W)

        self.entryCat = Entry(entryFrame)
        self.entryCat.bind('<Button>', lambda event : self.entryCat.delete(0,END))

        if (self.process == "Edit Item"):
            self.entryCat.insert(END, self.menuCat)
        else:
            self.entryCat.insert(0, catList[0][0])
        self.entryCat.grid(column=1, row=2, sticky=E)

        listboxScrollbar = Scrollbar(entryFrame, orient=VERTICAL)
        listboxCat = Listbox(entryFrame, yscrollcommand=listboxScrollbar.set)
        listboxScrollbar.configure(command=listboxCat.yview)
        listboxScrollbar.grid(column=2,row=3,sticky=NSEW)
        listboxCat.grid(column=1, row=3)

        def setEntryCatText(selection):
            self.entryCat.delete(0, END)
            self.entryCat.insert(0, selection)

        listboxCat.bind('<<ListboxSelect>>', lambda event : setEntryCatText(listboxCat.get(ANCHOR)))

        for cat in catList:
            listboxCat.insert(END, cat[0])
            if (self.process == "Edit Item" and cat[0] == self.menuCat):
                listboxCat.selection_set(END)
            elif (self.process == "Add Item"):
                listboxCat.selection_set(0)

        # PRICE ENTRY
        lbl=Label(entryFrame, text="Price: ")
        lbl.grid(column=0, row=4, sticky=W)

        self.entryPrice = Entry(entryFrame)
        self.entryPrice.grid(column=1, row=4)

        if (self.process == "Edit Item"):
            self.entryPrice.insert(END, self.menuPrice)
        if (self.process == "Edit Item"):
            self.entryPrice.insert(END, 0)

        # BUTTONS
        btnFrame = Frame(frame)
        btnFrame.pack(anchor=E, pady=[20,0])

        btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        btn.pack(side=RIGHT)

        btn = Button(btnFrame, text=self.process, command= self.genAddDone if self.process=="Add Item" else self.genEditDone)
        btn.pack(side=RIGHT, padx=10)

    def genRemoveDone(self):
        deleteMenuItem = ("DELETE FROM menu WHERE menuNo = %s" % self.menuNo)
        self.db.set(deleteMenuItem)
        msgbox.showinfo(self.process, "Item Removed")
        self.updateAndDestroy()

    def genAddDone(self):
        name = self.entryName.get()
        cat = self.entryCat.get()
        price = self.entryPrice.get()

        addMenuItem = ("INSERT INTO menu(name, category, price) VALUES (\"%s\", \"%s\", %s)" % (name, cat, price))
        self.db.set(addMenuItem)
        msgbox.showinfo(self.process, "Item Added")
        self.updateAndDestroy()

    def genEditDone(self):
        name = self.entryName.get()
        cat = self.entryCat.get()
        price = self.entryPrice.get()

        updateMenuItem = ("UPDATE menu SET name = \"%s\", category = \"%s\", price = %s WHERE menuNo = %s" % (name, cat, price, self.menuNo))
        self.db.set(updateMenuItem)
        msgbox.showinfo(self.process, "Item Edited")
        self.updateAndDestroy()

    def updateAndDestroy(self):
        self.top.destroy()
        self.parentClass.generateMenuTree()
        del self

class MenuWindow():
    def __init__ (self, master):
        self.rmCol = "#6"
        self.editCol = "#5"

        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master = master
        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Menu")

        frame = Frame(master)
        frame.pack(side=TOP, fill=X)
        self.init_backBtn(frame)

        self.treeFrame = Frame(master)
        self.treeFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.init_menuTree()

        self.generateMenuTree()

        self.pc.setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2, command=self.master.destroy)
        self.btnBack.pack(side=TOP, fill=BOTH)
    
    def init_menuTree(self):
        self.menuFrame = Frame(self.treeFrame)
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
        self.menuTree.heading("edit", text="")
        self.menuTree.heading("rm", text="")

        self.menuTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.menuFrame, orient=VERTICAL, command=self.menuTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.menuTree.configure(yscrollcommand=self.scrollBar.set)

    def generateMenuTree(self):
        self.menuTree.bind("<Button-1>", self.processClick)
        ttk.Style().configure("Treeview", rowheight=50)
        self.menuTree.delete(*self.menuTree.get_children())

        self.dbResults = self.db.get("SELECT menuNo, category, name, price FROM menu")

        self.listInc=1
        self.menuTree.insert("", tk.END, 0, value=("","","","","Add Item","Add Item"))

        for row in self.dbResults:
            _values = [self.listInc, row[1], row[2], row[3], "Edit this", "Remove this"]
            self.menuTree.insert("", tk.END, self.listInc, value=_values)
            self.listInc+=1

        self.menuTree.insert("", tk.END, self.listInc, value=("","","","","Add Item","Add Item"))

    def processClick(self, event):
        item = self.menuTree.identify('item', event.x, event.y)
        row = self.menuTree.identify_row(event.y)
        col = self.menuTree.identify_column(event.x)
        popup = PopupMenu(self.master, self)

        if row.isnumeric():
            if int(row) > 0 and int(row) <= len(self.dbResults):
                elem = int(row)-1
                if (col == self.rmCol):
                    popup.popWindow("Remove Item", self.dbResults[elem])
                elif (col == self.editCol):
                    popup.popWindow("Edit Item", self.dbResults[elem])
            elif (col == self.rmCol or col == self.editCol):
                popup.popWindow("Add Item", None)

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    menu = MenuWindow(root)
    root.mainloop()
