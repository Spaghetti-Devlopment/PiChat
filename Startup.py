#Main Systems
import threading;
from UI import UiSetup;
#UI
from tkinter import *;
import threading;

class startUp:
    serveraddress = 0
    username = ""
    uiInfo = UiSetup()

    connectFunction = set
    clientData = set

    def startUpClient(self, clientFunction, clientData):
        uiThread = threading.Thread(target=self.uiInfo.connectUiIp, args=(self.setIp,))
        uiThread.daemon = False
        uiThread.start()

        self.clientData = clientData
        self.connectFunction = clientFunction

    def clientStartup(self):
        #UI
        self.uiInfo.connectUiIp(self.setIp)

    def setIp(self, address):
        self.serveraddress = address
        print("Server Address Is: " + address)
        #Start Next UI
        self.uiInfo.connectUsernameUi(self.serveraddress, self.setUsername)

    def setUsername(self, username):
        #Make Sure Username Isn't Blank
        if(username == ""):
            username = "I Didn't Set A Username Because I'm Dumb"
        #Set Up Username
        self.username = username
        print("Username Is: " + username)
        self.connect(self.serveraddress, self.username)

    def connect(self, address, username):
        self.uiInfo.connectionHandler(address)

        self.connectFunction()

    #Other Functions
    def getUsername(self):
        return self.username

    def getIp(self):
        return self.serveraddress
