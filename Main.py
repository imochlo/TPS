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
import Dashboard
import Menu
import Reports

CWD=os.getcwd()

class StartupWindow():

    PAD_FRBTN_X = 40
    PAD_FRBTN_Y = 40
    PAD_FRLB_X = 30
    PAD_FRLB_Y = [10,40]
    BTN_HEIGHT = 5
    BTN_WIDTH = 10

    def __init__ (self, master):
        self.master=master
        master.title("TPSys")
        self.init_label(master)
        self.init_buttons(master)

    def init_label(self, master):
        self.lblFrame = Frame(master)
        self.lblFrame.pack(side=BOTTOM, padx=self.PAD_FRLB_X, pady=self.PAD_FRLB_Y)
        self.lblMain = Label(self.lblFrame, text = "Welcome to TPSys. Hover over a task.")
        self.lblMain.pack()

    def init_buttons(self, frame):
        self.btnFrame = Frame(frame)
        self.btnFrame.pack(padx=self.PAD_FRBTN_X, pady=self.PAD_FRBTN_Y)

        self.btnDashboard = Button(self.btnFrame, text = "Dashboard", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, command=self.genDashboard)
        self.btnDashboard.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnDashboard.bind('<Enter>', lambda event: self.lblMain.configure(text="Input new transactions in the dashboard"))
        self.btnDashboard.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))

        self.btnMenu = Button(self.btnFrame, text = "Menu" , justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, command=self.genMenu)
        self.btnMenu.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnMenu.bind('<Enter>', lambda event: self.lblMain.configure(text="Add or edit menu items"))
        self.btnMenu.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))

        self.btnReports = Button(self.btnFrame, text = "Reports", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, comman=self.genReports)
        self.btnReports.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        self.btnReports.bind('<Enter>', lambda event: self.lblMain.configure(text="Generate or view sales, customer, or order reports"))
        self.btnReports.bind('<Leave>', lambda event: self.lblMain.configure(text="Welcome to TPSys. Hover over a task."))

    def genDashboard(self):
        newFrame = Toplevel(self.master)
        dashBoardWindow = Dashboard.DashboardWindow(newFrame)

    def genMenu(self):
        newFrame = Toplevel(self.master)
        menuWindow = Menu.MenuWindow(newFrame)

    def genReports(self):
        newFrame = Toplevel(self.master)
        reportsWindow = Reports.ReportsWindow(newFrame)


if __name__ == "__main__":
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    startup = StartupWindow(root)
    root.mainloop()
