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
        self.init_buttons(master)
        self.init_label(master)

    def init_label(self, master):
        lblFrame = Frame(master)
        lblFrame.pack(side=BOTTOM, padx=self.PAD_FRLB_X, pady=self.PAD_FRLB_Y)
        self.lblInstructions = Label(lblFrame, text = "Welcome to TPSys. Hover over a task.")
        self.lblInstructions.pack()

    def init_buttons(self, frame):
        btnsFrame = Frame(frame)
        btnsFrame.pack(padx=self.PAD_FRBTN_X, pady=self.PAD_FRBTN_Y)

        btnDashboard = Button(btnsFrame, text = "Dashboard", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, command=self.genDashboard)
        btnDashboard.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        btnDashboard.bind('<Enter>', lambda event: self.lblInstructions.configure(text="Input new transactions in the dashboard"))
        btnDashboard.bind('<Leave>', lambda event: self.lblInstructions.configure(text="Welcome to TPSys. Hover over a task."))

        btnMenu = Button(btnsFrame, text = "Menu" , justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, command=self.genMenu)
        btnMenu.pack(side=LEFT, padx=self.PAD_FRBTN_X)

        btnMenu.bind('<Enter>', lambda event: self.lblInstructions.configure(text="Add or edit menu items"))
        btnMenu.bind('<Leave>', lambda event: self.lblInstructions.configure(text="Welcome to TPSys. Hover over a task."))

        btnReports = Button(btnsFrame, text = "Reports", justify=CENTER, width=self.BTN_WIDTH, height = self.BTN_HEIGHT, comman=self.genReports)
        btnReports.pack(side=LEFT, padx=self.PAD_FRBTN_X)
        btnReports.bind('<Enter>', lambda event: self.lblInstructions.configure(text="Generate or view sales, customer, or order reports"))
        btnReports.bind('<Leave>', lambda event: self.lblInstructions.configure(text="Welcome to TPSys. Hover over a task."))

    def genDashboard(self):
        topFrame = Toplevel(self.master)
        dashBoardWindow = Dashboard.DashboardWindow(topFrame)

    def genMenu(self):
        topFrame = Toplevel(self.master)
        menuWindow = Menu.MenuWindow(topFrame)

    def genReports(self):
        topFrame = Toplevel(self.master)
        reportsWindow = Reports.ReportsWindow(topFrame)


if __name__ == "__main__":
    root = Tk()
    root.bind("<Control-w>", lambda event: root.destroy())

    startup = StartupWindow(root)
    root.mainloop()
