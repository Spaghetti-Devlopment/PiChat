#Main Systems
import threading;
from UI import UiSetup;
#UI
from tkinter import *;
import threading;

class startUp:
    Serveraddress = 0
    username = ""
    uiInfo = UiSetup()
    #Start Up
    def startUpServer(self):
        uiThread = threading.Thread(target=self.uiInfo.makingServer)
        uiThread.daemon = True
        uiThread.start()