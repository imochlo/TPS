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
processTest = "Add Item"
menuItem = "4"

no_index=0
name_index=1
cat_index=2
price_index=3
image_index=4

class PopupMenu():
    def __init__ (self, master, parentClass):
        self.master=master
        #self.master.bind("<Control-w>", lambda event: master.destroy())
        self.parentClass = parentClass

        self.pc = Services.Local(self.master)
        self.db = Services.Db()

    def popWindow(self, process, menuItem):
        self.top=Toplevel(self.master)
        self.top.bind("<Control-w>", lambda event: self.top.destroy())

        self.process=process
        self.menuItem=menuItem
        self.top.title(process)

        frame = Frame(self.top)
        frame.pack(padx=[70,100], pady=50, expand=True)

        if (process == "Remove Item"):
            self.genRemoveWindow(frame)
        else:
            self.genTemplateWindow(frame)

        return True

    def genRemoveWindow(self, frame):
        lblFrame = Frame(frame)
        lblFrame.pack()

        lbl = Label(lblFrame, text="Are you sure you want to delete this item?")
        lbl.pack(side=TOP, pady=[0,20])
        command = ("SELECT * FROM menu WHERE menuNo = " + self.menuItem)
        result = self.db.get(command)

        lbl = Label(lblFrame, text="Name: " + result[0][1])
        lbl.pack(side=TOP, anchor=W)
        lbl = Label(lblFrame, text="Category: " + result[0][2])
        lbl.pack(side=TOP, anchor=W)
        lbl = Label(lblFrame, text="Price: " + str(result[0][3]))
        lbl.pack(side=TOP, anchor=W)

        btnFrame = Frame(frame)
        btnFrame.pack(anchor=E, side=TOP, pady=[20,0])

        self.btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        self.btn.pack(side=RIGHT)
        self.btn = Button(btnFrame, text="Remove", command=lambda : self.genRemoveDone)
        self.btn.pack(side=RIGHT, padx=10)

    def genTemplateWindow(self, frame):
        self.cat_list = self.db.get("SELECT DISTINCT category FROM menu")
        if (self.process == "Edit Item"):
            result_list = self.db.get("SELECT * FROM menu WHERE menuNo = " + self.menuItem)

        entryFrame = Frame(frame)
        entryFrame.pack(anchor=W,expand=True, fill=BOTH)

        # NAME ENTRY
        lbl=Label(entryFrame, text="Name: ")
        lbl.grid(column=0, row=0, sticky=W)
        self.entryName = Entry(entryFrame)
        self.entryName.grid(column=1, row=0)
        if (self.process == "Edit Item"):
            self.entryName.insert(END, result_list[0][name_index])

        # CATEGORY ENTRY
        lbl=Label(entryFrame, text="Category: ")
        lbl.grid(column=0, row=2, sticky=W)

        self.entryCat = Entry(entryFrame)
        if (self.process == "Edit Item"):
            self.entryCat.insert(END, result_list[0][cat_index])
        self.entryCat.grid(column=1, row=2, sticky=E)
        self.entryCat.bind('<Button>', lambda event : self.entryCat.delete(0,END))

        listboxScrollbar = Scrollbar(entryFrame, orient=VERTICAL)
        self.listboxCat = Listbox(entryFrame, yscrollcommand=listboxScrollbar.set)
        listboxScrollbar.configure(command=self.listboxCat.yview)
        listboxScrollbar.grid(column=2,row=3,sticky=NSEW)
        self.listboxCat.grid(column=1, row=3)
        self.listboxCat.bind('<<ListboxSelect>>', self.setCatText)

        for cat in self.cat_list:
            self.listboxCat.insert(END, cat[0])

        # PRICE ENTRY
        lbl=Label(entryFrame, text="Price: ")
        lbl.grid(column=0, row=4, sticky=W)

        self.entryPrice = Entry(entryFrame)
        if (self.process == "Edit Item"):
            self.entryPrice.insert(END, result_list[0][price_index])
        self.entryPrice.grid(column=1, row=4)

        # BUTTONS
        btnFrame = Frame(frame)
        btnFrame.pack(anchor=E, pady=[20,0])

        self.btn = Button(btnFrame, text="Cancel", command=self.top.destroy)
        self.btn.pack(side=RIGHT)

        self.btn = Button(btnFrame, text=self.process, command= self.genAddDone if self.process=="Add Item" else self.genEditDone)
        self.btn.pack(side=RIGHT, padx=10)

    def setCatText(self, event):
        self.entryCat.delete(0, END)
        self.entryCat.insert(0, self.listboxCat.get(self.listboxCat.curselection()))

    def genRemoveDone(self):
        command = ("DELETE FROM menu WHERE menuNo = " + self.menuItem)
        self.db.set(command)
        self.db.get("SELECT * FROM Menu")
        msgbox.showinfo(self.process, "Item Removed\n\n" + command)
        self.updateAndDestroy()

    def genAddDone(self):
        name = self.entryName.get()
        cat = self.entryCat.get()
        price = self.entryPrice.get()
        command = ("INSERT INTO menu(name, category, price) VALUES (\"%s\", \"%s\", %s)" % (name, cat, price))
        self.db.set(command)
        self.db.get("SELECT * FROM Menu")
        msgbox.showinfo(self.process, "Item Added\n\n" + command)
        self.updateAndDestroy()

    def genEditDone(self):
        name = self.entryName.get()
        cat = self.entryCat.get()
        price = self.entryPrice.get()
        command = ("UPDATE menu SET name = \"%s\", category = \"%s\", price = %s WHERE menuNo = %s" % (name, cat, price, self.menuItem))
        self.db.set(command)
        self.db.get("SELECT * FROM Menu")
        msgbox.showinfo(self.process, "Item Edited\n\n" + command)
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
        self.menuTree.heading("edit", text="Edit")
        self.menuTree.heading("rm", text="Add/Remove")

        self.menuTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.menuFrame, orient=VERTICAL, command=self.menuTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.menuTree.configure(yscrollcommand=self.scrollBar.set)

    def generateMenuTree(self):
        self.menuTree.bind("<Button-1>", self.processClick)
        ttk.Style().configure("Treeview", rowheight=50)
        self.menuTree.delete(*self.menuTree.get_children())

        self.dbResults = self.db.get("SELECT * FROM menu")

        listInc=1
        self.menuTree.insert("", tk.END, 0, value=("","","","","","Add Item"))
        for row in self.dbResults:
            _values = [listInc, row[cat_index], row[name_index], row[price_index], "Edit this", "Remove this"]
            self.menuTree.insert("", tk.END, row[0], value=_values)
            listInc+=1

        self.menuTree.insert("", tk.END, row[0]+1, value=("","","","","","Add Item"))

    def processClick(self, event):
        item = self.menuTree.identify('item', event.x, event.y)
        row = self.menuTree.identify_row(event.y)
        col = self.menuTree.identify_column(event.x)
        popup = PopupMenu(self.master, self)
        if (col == self.rmCol):
            if any(row == str(elem[0]) for elem in self.dbResults):
                popup.popWindow("Remove Item",row)
            else:
                popup.popWindow("Add Item", row)
        if (col == self.editCol and any(row == str(elem[0]) for elem in self.dbResults)):
            popup.popWindow("Edit Item", row)

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    menu = MenuWindow(root)
    root.mainloop()
