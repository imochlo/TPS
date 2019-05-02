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
        frame.pack(side=TOP, fill=X, pady=30, padx=50)
        self.init_filter(frame)
        self.init_reportBtns(frame)

        frame = Frame(master, background="yellow")
        frame.pack(side=TOP, fill=BOTH, expand=True)

        self.pc.setFullScreen(master)

    def init_backBtn(self, frame):
        self.btnBack = Button(frame, text="Back to main window", height=2)
        self.btnBack.pack(side=TOP, fill=BOTH)

    def init_filter(self,master):
        self.filterFrame=Frame(master)
        self.filterFrame.pack(anchor=W)

        durationOpt = IntVar()
        self.rdbtn1 = Radiobutton(self.filterFrame, text="Generate Today    ", value=1, variable=durationOpt)
        self.rdbtn1.grid(column=0, row=0)

        self.rdbtn2 = Radiobutton(self.filterFrame, text="Generate Duration", value=2, variable=durationOpt)
        self.rdbtn2.grid(column=0, row=1)

        self.lblStartMonth = Label(self.filterFrame, text="Start Date:")
        self.lblStartMonth.grid(column=0, row=2, sticky=E)

        self.calStart = DateEntry(self.filterFrame)
        self.calStart.grid(column=1, row=2)

        self.lblEndMonth = Label(self.filterFrame, text="End Date:")
        self.lblEndMonth.grid(column=0, row=3, sticky=E)

        self.calEnd = DateEntry(self.filterFrame)
        self.calEnd.grid(column=1, row=3)

    def init_reportBtns(self, frame):
        self.btnFrame=Frame(frame)
        self.btnFrame.pack(anchor=W, pady=10)

        self.genBtn = Button(self.btnFrame, text="Generate Sales Report")
        self.genBtn.pack(side=LEFT, padx=[0,20])

        self.genBtn = Button(self.btnFrame, text="Generate Orders Report")
        self.genBtn.pack(side=LEFT, padx=[0,20])

        self.genBtn = Button(self.btnFrame, text="Generate Customers Report")
        self.genBtn.pack(side=LEFT)

    def generate_list(self,master):
        self.reportFrame = Frame(master)
        self.reportFrame.pack(side=BOTTOM, expand=True, fill=Y, pady=200)

        self.reportTree = ttk.Treeview(self.reportFrame, column=("no","cat","name","price","edit","rm"), show='headings', padding=50)

def quit(event):
        root.quit()

def setFullScreen(window):
    window.geometry("%dx%d" % (SCRN_W, SCRN_H))

if __name__ == '__main__':
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    pc = Services.Local(root)

    reports = ReportsWindow(root)
    root.mainloop()
