import sys
sys.path.append("/home/abrar11648/darkflow/")
from gonojowar import *


import os
import subprocess
import cv2
from concurrent.futures import ThreadPoolExecutor
import time
from tkinter import *
import threading



class gui():

    def __init__(self, master):

        master.wm_title('EYE TRACKER APPLICATION')

        varPID = StringVar()
        varPID.set(os.getpid())

        labelPidTitle = Label(master, text='PID serial')
        labelPidSerial = Label(master, textvariable= varPID)
        buttonRun = Button(master, text='Track EYE', command = self.runTracker)
        self.textBox = Text(master, height=25, width=40)
        bar = Scrollbar(master)
        bar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=bar.set)

        labelPidTitle.grid(row=0, column=0, sticky=W)
        labelPidSerial.grid(row=0, column=2, sticky=W)
        buttonRun.grid(row=1, column=1, sticky=W)
        self.textBox.grid(row=2, rowspan=3, columnspan=3)
        bar.grid(row=2, column=3, rowspan=3, columnspan=1, sticky=N + S + W)


        master.geometry('300x300')

        mainloop()

    def insertBox(self):

        file = open('dataText', 'r')

        while(True):
            text = file.read()

            textList = text.split('\n')

            self.textBox.insert(END, textList[0])
            master.update_idletasks()

    def runTracker(self):

        threading.Thread(target=classifier).start()
        self.insertBox()



master = Tk()

gui(master)