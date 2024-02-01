from tkinter import *;
from tkinter import scrolledtext
import threading;
from time import sleep
import StringHanderAdvanced as stringFunctions
#UI
from UserSettings import clientSettingsUi
#Updating UI
class updatingUi:

    def updateUiTextBox(self, uiElement, textBox, stockText):
        stopUpdatingUsingTextBox = False
        while stopUpdatingUsingTextBox == False:
            try:
                uiElement["text"] = stockText + textBox.get()
                sleep(0.1)
            except:
                stopUpdatingUsingTextBox = True

    def updateUiLabel(self, uiElement, messageList, waitTime):
        stopUpdatingUiLabels = False
        while stopUpdatingUiLabels == False:
            for text in messageList:
                try:
                    uiElement["text"] = text
                    sleep(waitTime)
                except:
                    stopUpdatingUiLabels = True

#UI Setup
class UiSetup:
    root = Tk
    uiUpdate = updatingUi()
    #Window Stuff
    normalX = 500
    normalY = 500
    timesBiggerX = 0
    timesBiggerY = 0

    def clearUi(self):
        for child in self.root.winfo_children():
            child.destroy()

    def startUp(self, startUp):
        self.root = Tk()
        #Colour
        self.root.configure(bg="#121013")
        #Size
        self.root.geometry("500x500")
        #Times Bigger
        self.timesBiggerX = self.root.winfo_width() / self.normalX
        self.timesBiggerY = self.root.winfo_height() / self.normalY
        #Title
        title = Label(self.root, text="Server Or Client", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))
        #Buttons
        #Server Button
        serverButton = Button(self.root, text="Server", bg="dark grey", fg="black", font=("arial", 20), command= startUp.serverStartup)
        serverButton.pack(padx=(0, 0), pady=(5, 0), fill=BOTH)
        #Client Button
        clientButton = Button(self.root, text="Client", bg="dark grey", fg="black", font=("arial", 20), command= startUp.clientStartup)
        clientButton.pack(padx=(0, 0), pady=(10, 0), fill=BOTH)
        #Start Main Loop
        self.root.mainloop()

    #Server Setting Up
    def makingServer(self):
        self.root = Tk()
        #Colour
        self.root.configure(bg="#121013")
        #Clear UI
        self.clearUi()
        #Setting Size
        self.root.geometry("750x500")
        #Starting
        starting = Label(self.root, text="Starting Server", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        starting.pack(padx=(0, 0), pady=(0, 0))
        #Animations
        messagesToShow = ["Starting Server.", "Starting Server..", "Starting Server...", "Starting Server.."]
        changingUiThread = threading.Thread(target=self.uiUpdate.updateUiLabel, args=(starting, messagesToShow, 0.5,))
        changingUiThread.daemon = True
        changingUiThread.start()

        self.root.mainloop()

    def madeServer(self):
        self.clearUi()
        #Title
        title = Label(self.root, text="Server Started", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))

        self.root.state(newstate='iconic')
        self.root.geometry("50x50")

    def failedToMakeServer(self):
        self.clearUi()
        #Title
        title = Label(self.root, text="We Failed To Make A Sever", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))

    def makingServerFailedAttempt(self, trys, errorCode):
        #Error
        error = Label(self.root, text="Failed To Make Server Attempt: " + str(trys) + " Error Code: " + str(errorCode), bg="#121013", fg="red", font=("arial", 13))
        error.pack(padx=(0, 0), pady=(0, 0))

    #Connecting Stuff Client
    def connectUiIp(self, buttonFunction):
        self.root = Tk()
        #Colour
        self.root.configure(bg="#121013")
        #Clear UI
        self.clearUi()
        #Connected
        self.connected = False
        #Window Size
        self.root.geometry("250x200")
        #Title
        title = Label(self.root, text="Client Setup", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0 ,0), fill=X)
        #Server Info Input
        serverInfoInput = Entry(self.root, bg="dark gray", fg="black", font=("Arial", 15))
        serverInfoInput.pack(padx=(0, 0), pady=(15, 0), fill=X)

        joinButton = Button(self.root, bg="dark gray", fg="black", font=("Arial", 15), command= lambda: buttonFunction(serverInfoInput.get()))
        joinButton.pack(padx=(0, 0), pady=(15, 0), fill=X)

        #Threading
        updateUiThread = threading.Thread(target=self.uiUpdate.updateUiTextBox, args=[joinButton, serverInfoInput, "Join: "])
        updateUiThread.daemon = True
        updateUiThread.start()

        self.root.mainloop()

    def connectUsernameUi(self, address, buttonFunction):
        self.clearUi()
        self.root.geometry("500x250")
        #Title
        title = Label(self.root, text="Client Setup", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))
        #Sevrer Info
        serverInfo = Label(self.root, text="Currently Connecting To: " + address, bg="#121013", fg="#9a9a9a", font=("Arial", 15))
        serverInfo.pack(padx=(0, 0), pady=(0, 5))
        #Username
        usernameInput = Entry(self.root, bg="dark gray", fg="black", font=("Arial", 15))
        usernameInput.pack(padx=(0, 0), pady=(10, 0))
        #Join Button
        joinButton = Button(self.root, text="Connect", bg="dark gray", fg="black", font=("Arial", 15), command = lambda: buttonFunction(usernameInput.get()))
        joinButton.pack(padx=(0, 0), pady=(10, 0))

    def connectionHandler(self, address):
        self.clearUi()
        self.root.geometry("750x500")
        #Title
        title = Label(self.root, text="Connecting To: " + address, bg="#121013", fg="#9a9a9a", font=("Arial Bold", 35))
        title.pack(padx=(0, 0), pady=(0, 0))
        #Connecting Text
        connectionText = Label(self.root, text="Connecting.", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 35))
        connectionText.pack(padx=(0, 0), pady=(25, 0))
        #Update Label
        connectionTexts = ["Connecting.", "Connecting..", "Connecting...", "Connecting.."]
        updateConnectionText = threading.Thread(target=self.uiUpdate.updateUiLabel, args=(connectionText, connectionTexts, 0.5))
        updateConnectionText.daemon = True
        updateConnectionText.start()

    def connectionFailed(self, address, startup):
        self.clearUi()
        #Title
        title = Label(self.root, text="Connection To: " + str(address) + " Failed", bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))
        #Connect To Another Server
        anotherServer = Button(self.root, text="Join Another Server", bg="dark gray", fg="black", font=("Arial Bold", 30), command= lambda: self.resetUi(startup))
        anotherServer.pack(padx=(0, 0), pady=(10, 0))

    def connectedToServer(self, address, startup):
        self.clearUi()
        #Title
        title = Label(self.root, text="Connected To: " + str(address), bg="#121013", fg="#9a9a9a", font=("Arial Bold", 30))
        title.pack(padx=(0, 0), pady=(0, 0))
        #Connect To Another Server
        anotherServer = Button(self.root, text="Join Another Server", bg="dark gray", fg="black", font=("Arial Bold", 30), command= lambda: self.resetUi(startup))
        anotherServer.pack(padx=(0, 0), pady=(10, 0))

    def connectionAttempt(self, address, trys, errorCode):
        #Error
        error = Label(self.root, text="Error Connecting To: " + address + " Try: " + str(trys) + " Error:" + str(errorCode), bg="#121013", fg="red", font=("Arial", 13))
        error.pack(padx=(0, 0), pady=(0, 0))

    def resetUi(self, startup):
        self.clearUi()
        self.connectUiIp(startup.setIp)

#Windows
class chatWindow:
    root = Tk 
    uiUpdating = updatingUi
    #Message Stuff
    messageCanvas = Canvas
    scrollbar = Scrollbar
    messageQueue = Label
    messageLabels = []
    y = 0
    #Message Formating
    #Message Showing 
    messageBox = scrolledtext.ScrolledText
    timeBeforeForcedSpace = 0
    #Window Stuff
    normalX = 500
    normalY = 500
    timesBiggerX = 0
    timesBiggerY = 0
    #Settings
    settings = clientSettingsUi
    #Setting Up
    def __init__(self, client):
        #Setup Ui Updating And User Settings
        self.uiUpdating = updatingUi()
        self.settings = clientSettingsUi()
        #Root Settings
        root = Tk()
        self.root = root
        root.configure(bg=self.settings.windowBackgroundColour)
        #Base Size
        self.root.geometry("500x500")
        self.normalX = 500
        self.normalY = 500
        #Client Setting
        client.chat = self
        #Setup UI
        self.setupUi(client, self.normalX, self.normalY)

    def setupUi(self, client, sizeX, sizeY):
        #Clear UI
        self.clearUi()
        #Times Bigger
        self.timesBiggerX = sizeX / self.normalX
        self.timesBiggerY = sizeY / self.normalY
        #Title
        appTitle = Label(self.root, text="PiText V0.1 Alpha", bg="#121013", fg="#9a9a9a", font=("arial bold", 30))
        #Message Box
        messageBox = scrolledtext.ScrolledText(self.root, bg="dark gray", fg="black", font=("arial", 15))
        self.messageBox = messageBox
        #Send Message
        sendMessageButton = Button(self.root, text="Send Message", bg="dark gray", fg="black", font=("arial", 20), command= lambda: client.clientSend.sendMessage(messageBox, client))       
        #Packing
        appTitle.place(x=0 * self.timesBiggerX, y=5 * self.timesBiggerY, width=500 * self.timesBiggerX, height=40 * self.timesBiggerY)
        sendMessageButton.place(x=0 * self.timesBiggerX, y=360 * self.timesBiggerY, width=500 * self.timesBiggerX, height=35 * self.timesBiggerY)
        self.messageBox.place(x=0 * self.timesBiggerX, y=405 * self.timesBiggerY, width=500 * self.timesBiggerX, height=70 * self.timesBiggerY)
        #Message Queue
        self.messageQueue = Label(self.root, text="", bg="#121013", fg="#9a9a9a", font=("arial light", 10))
        self.messageQueue.place(x=0 * self.timesBiggerX, y=485 * self.timesBiggerY, width=400 * self.timesBiggerX, height=15 * self.timesBiggerY)
        #Message Box Setup
        #self.messageBox.bind("<Return>", lambda event, messageBoxText=self.messageBox, clientSet=client: client.clientSend.sendMessage(messageBoxText, clientSet))
        #UI Setup
        self.labelScrollBar(client.messages)
        #Change UI
        changeUi = Button(self.root, text="Recalculate UI Scale", bg="#121013", fg="#9a9a9a", font=("arial light", 10), command = lambda: self.reloadUi(client))
        changeUi.pack(side=BOTTOM)
        #Run Main Loop
        self.root.mainloop()

    def reloadUi(self, client):
       #Window Size
       self.y = 0
       #Print Values
       print(str(self.root.winfo_width()) + "X" + str(self.root.winfo_height()))
       #Change UI
       self.setupUi(client, self.root.winfo_width(), self.root.winfo_height())

    def labelScrollBar(self, messageList):
        #Setup Canvas
        self.messageCanvas = Canvas(self.root, bg="#121013")
        self.messageCanvas.place(x=0 * self.timesBiggerX, y=50 * self.timesBiggerY, width=500 * self.timesBiggerY, height=300 * self.timesBiggerY)
       
        #Adding Old Messages
        newLabelList = []
        for message in self.messageLabels:
            newLabelList.append(Label(self.messageCanvas, text="", compound=RIGHT, bg=self.settings.textBackgroundColour, fg=self.settings.textColour, font=(self.settings.font, self.settings.fontSize)))
        self.messageLabels = newLabelList

        self.addToCanvas(messageList)
        #Setting Up Scrollbar
        self.scrollbar = Scrollbar(self.messageCanvas, orient=VERTICAL, command=self.messageCanvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        #Canvas Config
        self.messageCanvas.config(yscrollcommand=self.scrollbar.set, scrollregion=(0, 0, 0, self.y))

    def cleanMessageList(self):
        #Clear Listbox
        self.messageCanvas.delete(0, END)

    #Messages
    def addToMessageList(self, indexOfMessage, client, replaceLastMessage):
        #Setting Main Value
        self.y = 0
        #Removing Old Messages
        if(replaceLastMessage):
            #Removing Last Value
            self.messageLabels.pop(0)
            self.messageCanvas.delete('0.0')
            client.messages.pop(0)

        #Making Label
        messageLabel = Label(self.messageCanvas, text="", compound=RIGHT, font=(self.settings.font, self.settings.fontSize), bg=self.settings.textBackgroundColour, fg=self.settings.textColour)
        self.messageLabels.insert(indexOfMessage, messageLabel)
        #Adding To Canvas
        self.addToCanvas(client.messages)

        #Scrollbar Setup Again
        self.messageCanvas.config(scrollregion=(0, 0, 0, self.y))
        self.scrollbar.config(command = self.messageCanvas.yview)

        #Send To Bottom
        self.messageCanvas.yview_moveto('1.0')

    def addToCanvas(self, messageList):
        #indexing
        index = 0
        #Adding Messages
        for message in self.messageLabels:
            #if(self.stop):
            #    self.stop = False
            #    return

            messageShow = stringFunctions.messageSpliter(self.settings.beforeSpaces, messageList[index])
            message["text"] = messageShow

            self.messageCanvas.create_window(0, self.y, window=message, anchor=NW)
            self.y += message.winfo_reqheight() + self.settings.messageSpacing
            index += 1

    def sendingMessage(self, queueLength):
        #Making Label
        if(queueLength >= 1):
            self.messageQueue["text"] = "Current Queue: " + str(queueLength)
        else:
            self.messageQueue["text"] = ""

    def clearUi(self):
        for child in self.root.winfo_children():
            child.destroy()
