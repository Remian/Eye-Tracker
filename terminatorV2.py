import os
import signal
from tkinter import *


class setGui():

    def __init__(self, master, *args, **kwargs):
        master.wm_title('Eye Tracker Manager')

        self.checkButtonState = IntVar()

        labelPid = Label(master, text='Enter PID')
        self.entryPid = Entry(master)
        buttonPid = Button(master, text='Terminate', command=self.kill)
        buttonFile = Button(master, text='Open Raw File', command=self.openFile())
        self.checkButton = Checkbutton(master, text="click to change state for raw file display", variable=self.checkButtonState)


        labelPid.grid(row = 0, column = 0, sticky=W)
        self.entryPid.grid(row= 0, column=1, sticky=W)
        buttonPid.grid(row= 0, column=2, sticky=W)
        self.checkButton.grid(row = 1, columnspan=3)
        buttonFile.grid(row = 2, column = 1)

        master.geometry('300x70')

        mainloop()

    def kill(self):
        pid = self.entryPid.get()
        pid = int(pid)
        os.kill(pid, signal.SIGKILL)

    def openFile(self):



        if self.checkButtonState == 1:
            os.popen('gedit dataText')


master = Tk()

setGui(master)






