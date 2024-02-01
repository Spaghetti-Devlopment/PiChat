#Threading
import threading as therad;
#Encryption
from Encryption import Encryptor
#UI
from UI import serverWindow
#Networking
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
#All Server Data
class sheredServerData:
    #End Points
    endpoint = TCP4ServerEndpoint
    #Messages
    messages = []
    messagesToSendClients = []
    #Classes
    encryptor = Encryptor
    #Networking Stuff
    connections = []
    connectionsUDP = []
    #Client Stuff
    clientIDs = []
    clientMessagesGot = []
    clientKeys = []
    #UDP
    startUdpPort = 2000
    #UI
    serverUiWindow = serverWindow
    #Making Core
    def __init__(self, encryptor, endpoint : TCP4ServerEndpoint):
        #Encryption
        self.encryptor = encryptor
        self.endpoint = endpoint
        #UI
        uiThread = therad.Thread(target=serverWindow, args=("e", "e", self,))
        uiThread.daemon = False
        uiThread.start()