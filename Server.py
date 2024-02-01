#Main
from PacketHandler import ServerPacketHandler;
from ServerSend import ServerSend
#Encryption
from Encryption import Encryptor
from Startup import startUp
#Other
from ShearedServerData import sheredServerData
#Networking
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as serverFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import UDPServer

class Server(Protocol):
    #Sever Data Pool
    serverData = sheredServerData
    #Classes
    packetHandler = ServerPacketHandler
    serverSend = ServerSend
    #Client Stuff
    connections = []
    clientId = 0
    #UDP
    udpPort = 0

    #Sever Setup
    def __init__(self, encryptor, serverDataPool):
        #Server Data
        self.serverData = serverDataPool
        #Main
        self.serverData.clientKeys.append(set)
        self.serverData.clientIDs.append(len(self.serverData.connections))
        self.serverData.clientMessagesGot.append(1)
        #Client Id
        self.clientId = len(self.serverData.connections)
        #Encryption And Sending
        self.serverSend = ServerSend()
        self.encryptor = encryptor
        #Server Packet Handler
        self.packetHandler = ServerPacketHandler(self.serverData, self)
        #Find Port
        self.udpPort = self.findEmptyPort(2000, 10)

    def findEmptyPort(self, startPort, maxPlayers):
        currentPort = startPort
        for i in range(maxPlayers):
            try:
                reactor.listenUDP(currentPort, UDPServer.UDPServer(self.encryptor, self.serverData, self))
                print("Started UDP Server On: " + str(currentPort))
                return currentPort
            except Exception as e:
                print("Failed To Start UDP Server On: " + str(currentPort) + " " + str(e))
                currentPort += 1

    ##Change Client Keys Every Minute
    #isChangingKey = False

    #def changeKeys(self):
    #    #Wait
    #    sleep(60000)
    #    #If No Clients Return 
    #    if(len(self.clientIDs) <= 0):
    #        #Add To Server Log
    #        self.serverUiWindow.addToServerLogs("Key Change Failed: No Clients Connected [0000PT]")
    #        #Run Again
    #        self.changeKeys()
    #        return

    #    self.isChangingKey = True
    #    print("Change Keys!")
    #    #Thread
    #    keyChangingThread = therad.Thread(target=self.encryptor.changeKeys())
    #    keyChangingThread.daemon = True
    #    keyChangingThread.start()
    #    #Changing Keys
    #    self.encryptor.changeKeys()
    #    self.serverSend.serverChangePublicKey(self.encryptor.publicKeyString)
    #    #Restarting Function
    #    self.isChangingKey = False
    #    self.changeKeys()

#New Networking Stuff
    def connectionMade(self):
        print("New Connection")
        self.serverData.connections.append((self, set))
        #Update Server Sending
        self.serverSend.updateServerInfo(self.serverData.connections, self.serverData.clientIDs)
        #Update Server Send
        self.serverSend.sendPublicKey(self.encryptor.publicKeyString, self.clientId)

        for server in self.connections:
            print(server.clientId)

    def connectionLost(self, reason):
        print("A User Has Lost Connection Reason: " + str(reason))

    def dataReceived(self, data: bytes):
        #Check If Encrypted
        try:
            data = self.encryptor.decryptPrivateKey(data)
            print(data)
        except Exception as e:
            pass
        #Handle Packet
        print(self.clientId)
        self.packetHandler.packetData(data, self.clientId)

#Core Networking
class ServerFactory(serverFactory):
    uiHandler = set
    encryptor = Encryptor
    dataPool = sheredServerData

    def __init__(self, uiHandler, endpoint):
        self.uiHandler = uiHandler
        #Encryption
        self.encryptorSetup(self.uiHandler)
        #Data Pool
        self.dataPool = sheredServerData(self.encryptor, endpoint)
        #UI
        self.uiHandler.madeServer()

    def buildProtocol(self, addr):
        self.dataPool.serverUiWindow.addToServerLogs("Connection Attempt From: " + str(addr))
        return Server(self.encryptor, self.dataPool)

    #Encryption
    def encryptorSetup(self, uiHandler):
        #Encyption
        print("Firing Up Encryptor...")
        try:
            self.encryptor = Encryptor()
            #Key Changing
            #keyChangingThread = therad.Thread(target=self.changeKeys)
            #keyChangingThread.daemon = True
            #keyChangingThread.start()

        except Exception as e:
            print("That's Odd Our Encryptor Had No Gas " + str(e))
            uiHandler.failedToMakeServer()
            return

if __name__ == '__main__':
    #Making Ui Stuff
    starting = startUp()
    starting.startUpServer()
    #Networking
    endpointTCP = TCP4ServerEndpoint(reactor, 2000)
    endpointTCP.listen(ServerFactory(starting.uiInfo, endpointTCP))
    reactor.run()