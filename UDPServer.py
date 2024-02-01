from ShearedServerData import sheredServerData
from ServerSend import ServerSend
#Networking
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from Encryption import Encryptor

class UDPServer(DatagramProtocol):
    encryptor = Encryptor
    tcpServer = set
    serverData = sheredServerData
    clientId = 0
    address = ""

    def __init__(self, encryptor, serverDataPool, tcpServer):
        self.encryptor = encryptor
        self.serverData = serverDataPool
        self.tcpServer = tcpServer

    def datagramReceived(self, data : bytes, addr):
        decryptedData = self.encryptor.decryptPrivateKey(data)
        if(decryptedData[0] == "First UDP Packet"):
            #Getting Id
            self.clientId = self.tcpServer.clientId
            #Address
            self.address = addr
            #Adding To Connections
            newConnection = [self.serverData.connections[self.clientId][0], self]
            self.serverData.connections[self.clientId] = newConnection
            #Update List
            self.tcpServer.serverSend.updateServerInfo(self.serverData.connections, self.serverData.clientIDs)
            #Adding To UDP List
            self.serverData.connectionsUDP.append(addr)
            print("New UDP Connection: " + str(addr))
        else:
            self.tcpServer.packetHandler.packetData(decryptedData, self.clientId)