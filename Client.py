from asyncio import DatagramProtocol
import threading as therad;
from tkinter import *;
from time import sleep;
#Packets/Server
from ClientSend import clientSend as ClientSend
from PacketHandler import PacketHandlerClient;
#UI
from UI import chatWindow
from Startup import startUp
#For Encription Stuff
from Encryption import Encryptor
#Networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import ClientFactory as clientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

#Client Stuff
class Client(Protocol):
    #Keys
    changingKeys = False
    serverPublicKey = set
    #Main Values
    clientSend = ClientSend
    encryptor = Encryptor
    packetHandler = PacketHandlerClient
    #UDP
    udpServer = set
    udpPort = 0
    #Server Info
    username = ""
    messages = []
    #Connection Stuff
    connected = False
    serverAddress = set
    #ID
    clientId = 0
    hasBeenWelcomed = False
    #UI
    chat = chatWindow

    def __init__(self, coreClientData, username):
        #Core
        self.clientSend = coreClientData.clientSend
        self.encryptor = coreClientData.encryptor
        self.packetHandler = PacketHandlerClient(self)
        #Username
        self.username = username

    #Start UDP
    def startUDP(self):
        reactor.listenUDP(0, UDPReciver(self))

    #New Networking Stuff
    def dataReceived(self, data: bytes):
        #Check If Encrypted
        try:
            data = self.encryptor.decryptPrivateKey(data)
        except Exception as e:
            print(e)
            pass
        #Handel Packet
        self.packetHandler.packetData(data);

class neededClientData:
    #Core
    encryptor = Encryptor
    clientSend = ClientSend

    def coreStartup(self):
        self.encryptor = Encryptor()
        self.clientSend = ClientSend()

class ClientFactory(clientFactory):
    uiHandler = set
    coreClientData = neededClientData
    username = "I Didn't Set A Username Because I'm Dumb"
    
    def __init__(self, uiHandler, coreClientData, username):
        #Setting Up Client
        self.uiHandler = uiHandler
        self.coreClientData = coreClientData
        self.username = username
        
    #Make Client Class
    def buildProtocol(self, addr):
        return Client(self.coreClientData, self.username)

class UDPReciver(DatagramProtocol):
    client = Client

    def __init__(self, client: Client):
        self.client = client
        self.client.udpServer = self

    def startProtocol(self):
        self.transport.connect("192.168.28.1", self.client.udpPort)
        #Encryptor
        packet = ["First UDP Packet", self.client.clientId]
        encryptedPacket = self.client.encryptor.encryptUsingPublicKey(packet, self.client.serverPublicKey)
        self.transport.write(encryptedPacket)

    def datagramReceived(self, data, addr):
        decryptedData = self.client.encryptor.decryptPrivateKey(data)
        self.client.packetHandler.packetData(decryptedData)

    def connectionRefused(self):
        print("Connection Refused")

def connect(coreClientData, uiInfo, username, ip, port):
    #Networking
    if __name__ == '__main__':
        endpoint = TCP4ClientEndpoint(reactor, ip, port)
        endpoint.connect(ClientFactory(uiInfo, coreClientData, username))
        reactor.run()
    else:
        print("Failed To Make Sever Not In Main Thread")

class connecting:

    startConnection = False

    def startConnecting(self):
        self.startConnection = True

if __name__ == '__main__':
    #Needed Stuff
    coreClientData = neededClientData()
    coreClientData.coreStartup()
    #Connecting Functions
    connection = connecting()
    #Making Ui Stuff
    starting = startUp()
    #Connecting
    starting.startUpClient(connection.startConnecting, coreClientData)
    #Wait Untill Condition
    while(connection.startConnection == False):
        sleep(1)

    connect(coreClientData, starting.uiInfo, starting.getUsername(), starting.getIp(), 2000)