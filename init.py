from tkinter import *
from tkinter import messagebox
PAD_FRBT_X = 40
PAD_FRBT_Y = 40
PAD_FRLB_X = 30
PAD_FRLB_Y = [10,40]
BT_X = 1
BT_HEIGHT = 5
BT_WIDTH = 10

def quit(event):
    window.quit()

def genDashboard():
    messagebox.showinfo("TPSys Dashboard", "Insert Dashboard Here")
def genMenu():
    messagebox.showinfo("TPSys Menu", "Insert Menu Here")
def genReports():
    messagebox.showinfo("TPSys Reports", "Insert Reports Here")

def printDashboardInfo(self):
    lblMain.configure(text="Input new transactions in the dashboard")

def printMenuInfo(self):
    lblMain.configure(text="Add or edit menu items")

def printReportsInfo(self):
    lblMain.configure(text="Generate or view sales, customer and order reports")

def printMain(self):
    lblMain.configure(text="Welcome to TPSys. Hover over a task.")

window = Tk()

window.bind("<Control-w>", quit)

window.title("TPSys")

frButtons = Frame(window)
frButtons.pack(padx=PAD_FRBT_X, pady=PAD_FRBT_Y)

frLabel = Frame(window)
frLabel.pack(side=BOTTOM, padx=PAD_FRLB_X, pady=PAD_FRLB_Y)

btDashboard  = Button(frButtons, text = "Dashboard", command = genDashboard, justify=CENTER, width = BT_WIDTH, height = BT_HEIGHT)
btDashboard.pack(side=LEFT, padx=PAD_FRBT_X)
btDashboard.bind('<Enter>', printDashboardInfo)
btDashboard.bind('<Leave>', printMain)

btMenu = Button(frButtons, text = "Menu", command = genMenu, justify=CENTER, width = BT_WIDTH, height = BT_HEIGHT)
btMenu.pack(side=LEFT, padx=PAD_FRBT_X)
btMenu.bind('<Enter>', printMenuInfo)
btMenu.bind('<Leave>', printMain)

btReports = Button(frButtons, text = "Reports", command = genReports, justify=CENTER, width = BT_WIDTH, height = BT_HEIGHT)
btReports.pack(side=LEFT, padx=PAD_FRBT_X)
btReports.bind('<Enter>', printReportsInfo)
btMenu.bind('<Leave>', printMain)

lblMain = Label(frLabel, text = "Welcome to TPSys. Hover over a task.")
lblMain.pack()

window.mainloop()
