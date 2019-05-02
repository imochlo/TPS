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
processTest = "Edit Item"
menuItem = "4"

class PopupMenu():
    def __init__ (self, master):
        self.master=master
        self.pc = Services.Local(self.master)
        self.db = Services.Db()
        self.master.bind("<Control-w>", lambda event: master.destroy())


    def popWindow(self, process, menuItem):
        self.process=process
        self.menuItem=menuItem
        self.master.title(process)

        frame = Frame(self.master)
        frame.pack(padx=[70,100], pady=50, expand=True)

        if (process == "Remove Item"):
            self.genRemoveWindow(frame)
        else:
            self.genTemplateWindow(frame)

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

        self.btn = Button(btnFrame, text="Cancel", command=self.master.destroy)
        self.btn.pack(side=RIGHT)
        self.btn = Button(btnFrame, text="Yes", command=self.genRemoveDone)
        self.btn.pack(side=RIGHT, padx=10)

    def genTemplateWindow(self, frame):
        entryFrame = Frame(frame)
        entryFrame.pack(anchor=W,expand=True, fill=BOTH)

        lbl=Label(entryFrame, text="Name: ")
        lbl.grid(column=0, row=0, stick=W)
        entryName = Entry(entryFrame)
        entryName.grid(column=1, row=0)

        lbl=Label(entryFrame, text="Category: ")
        lbl.grid(column=0, row=2, stick=W)
        entryCat = Entry(entryFrame)
        entryCat.grid(column=1, row=2)

        lbl=Label(entryFrame, text="Price: ")
        lbl.grid(column=0, row=3, stick=W)
        entryPrice = Entry(entryFrame)
        entryPrice.grid(column=1, row=3)

        btnFrame = Frame(frame)
        btnFrame.pack(anchor=E, pady=[20,0])

        self.btn = Button(btnFrame, text="Cancel", command=self.master.destroy)
        self.btn.pack(side=RIGHT)

        #genUpdateDone = lambda x : (x == "Add Item") ? self.genAddDone : self.genEditDone
        self.btn = Button(btnFrame, text=self.process, command= self.genAddDone if self.process=="Add Item" else self.genEditDone)
        self.btn.pack(side=RIGHT, padx=10)

    def genRemoveDone(self):
        command = ("DELETE FROM menu WHERE menuNo = " + self.menuItem)
        #self.db.set(command)
        msgbox.showinfo(self.process, "Item Removed\n\n" + command)

    def genAddDone(self):
        msgbox.showinfo("add", "add")

    def genEditDone(self):
        msgbox.showinfo("edit", "edit")

class MenuWindow():
    def __init__ (self, master):
        self.no_index=0
        self.name_index=1
        self.cat_index=2
        self.price_index=3
        self.image_index=4
        
        self.rmCol = "#6"
        self.editCol = "#5"

        self.pc = Services.Local(master)
        self.db = Services.Db()

        self.master = master
        self.master.bind("<Control-w>", lambda event: master.destroy())
        self.master.title("TPSys Menu")

        frame = Frame(master, background="black")
        frame.pack(side=TOP, fill=X)
        self.init_backBtn(frame)

        frame = Frame(master, background="red")
        frame.pack(side=TOP, fill=BOTH, expand=True)
        self.init_menuTree(frame)

        self.generate_menuTree()

        self.pc.setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2)
        self.btnBack.pack(side=TOP, fill=BOTH)
    
    #def init_fileMenu(self, frame):
    #    self.file_item = Menu(frame, tearoff=0)
    #    self.file_item.add_command(label='Add Item')

    #    self.file_list = Menu(frame)
    #    self.file_list.add_cascade(label='File', menu=self.file_item)
    #    master.config(menu=self.file_list)

    def init_menuTree(self, frame):
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

        self.menuTree.bind("<Button-1>", self.processClick)
        self.menuTree.pack(side=LEFT, expand=True, fill=BOTH)

        self.scrollBar = ttk.Scrollbar(self.menuFrame, orient=VERTICAL, command=self.menuTree.yview)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.menuTree.configure(yscrollcommand=self.scrollBar.set)

    def generate_menuTree(self):
        ttk.Style().configure("Treeview", rowheight=50)
        self.menuTree.delete(*self.menuTree.get_children())

        self.dbResults = self.db.get("SELECT * FROM menu")

        self.menuTree.insert("", tk.END, 0, value=("","","","","","Add Item"))
        self.listCounter=1
        for row in self.dbResults:
            _values = [row[self.no_index], row[self.cat_index], row[self.name_index], row[self.price_index], "Edit this", "Remove this"]
            #_values = [counter, row[self.cat_index], row[self.name_index], row[self.price_index], "Edit this", "Remove this"]
            self.listCounter+=1

            self.menuTree.insert("", tk.END, row[0], value=_values)

        self.menuTree.insert("", tk.END, row[0]+1, value=("","","","","","Add Item"))

    def processClick(self, event):
        item = self.menuTree.identify('item', event.x, event.y)
        row = self.menuTree.identify_row(event.y)
        col = self.menuTree.identify_column(event.x)
        popup = PopupMenu()
        if (col == self.rmCol):
            if (row == "0") or (row == str(len(self.dbResults)+1)):
                msgbox.showinfo("add", "add")
            else:
                msgbox.showinfo("delete",row)
        if (col == self.editCol):
            msgbox.showinfo("edit", row)

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    #menu = MenuWindow(root)
    test = PopupMenu(root)
    test.popWindow(processTest, menuItem)
    root.mainloop()
