import json
from time import sleep
from Cryptodome.PublicKey import RSA

class ServerPacketHandler:

    currentPacketData = set
    server = set
    serverData = set

    def __init__(self, serverData, server):
        self.serverData = serverData
        self.server = server

    def packetData(self, packetData, clientId):
        if(self.checkIfJson(packetData) == True):
            packetName = packetData[0]
            self.currentPacketData = packetData

            function = getattr(self, packetName, lambda: self.packetNotFound(packetName))
            function(clientId)
        else:
            print("Decoding Key")
            #This is ONLY Used For Getting Keys <:(
            #Decoding
            print(packetData)
            decodedData = bytes.decode(packetData, 'utf-8')
            commandKey = decodedData.split(' ', 1)
            #Getting Packet Name
            packetName = commandKey[0]
            #Getting Function
            function = getattr(self, packetName, lambda: self.packetNotFound(packetName))
            function(commandKey[1], self.server.clientId)
   
    #Check If Json
    def checkIfJson(self, file):
        try:
            file = json.dumps(file)
            json.loads(file)
        except:
            return False
        return True

    #Handeling Packets
    def message(self, clientId):
        #Formatting Message
        message = self.currentPacketData[1]

        #Adding To Sever Logs
        self.serverData.serverUiWindow.addToServerLogs("Client: " + str(clientId) + " Said: " + message)
        #Add To Message List
        self.serverData.messages.append(message)
        #Spliting Message
        #Sending The Data Off
        for id in self.serverData.clientIDs:
            #Setting Up
            needsToReplaceLastMessage = False
            if(self.serverData.clientMessagesGot[id] > 50):
                 needsToReplaceLastMessage = True
            #Making New Paacket
            packet = ["message", message, self.serverData.clientMessagesGot[id], needsToReplaceLastMessage]
            #Try Sending Packet
            print(self.serverData.connections)
            try:
                #Encrypt Data
                encryptedData = self.serverData.encryptor.encryptUsingPublicKey(packet, self.serverData.clientKeys[id])
                self.server.serverSend.sendMessage(encryptedData, self.serverData.connections[id][1])
                print("client: " + str(id) + " Has Gotten: " + str(self.serverData.clientMessagesGot[id]) + " Messages")
                #Make Sure Index Is No More Then 50
                if(needsToReplaceLastMessage == False):
                    self.serverData.clientMessagesGot[id] += 1
            except Exception as e:
                self.serverData.serverUiWindow.addToServerLogs("Error Sending Message Packet To: " + str(id) + " Error: " + str(e))
        #Wait Before Sending Next
        sleep(0.05)

    def serverKeyRequest(self, clientId):
        #Add To Server Logs
        message = "User: " + str(clientId) + " Has Made A Public Key Request"
        self.serverData.serverUiWindow.addToServerLogs(message)
        #Send Key
        self.serverData.serverSend.sendPublicKey(self.serverData.encryptor.publicKeyString, clientId)

    def clientPublicKeyFirst(self, key, clientId):
        #Import Key
        publicClientKey = RSA.importKey(key)
        self.serverData.clientKeys[clientId] = publicClientKey
        #Add To Server Logs
        message = "Got Client  For: " + str(clientId) + " Public Key: " + str(publicClientKey)
        self.serverData.serverUiWindow.addToServerLogs(message)
        #Welcome User
        if(len(self.serverData.messagesToSendClients) >= 50):
                print("Removing Item")
                #Remove First Item
                self.serverData.messagesToSendClients.pop(0)

        #Add To Message List
        self.serverData.messagesToSendClients.append("Welcomed Someone!")
        self.server.serverSend.welcome("Welcome To The Server!", clientId, self.serverData.connections[clientId][0].udpPort, self.serverData.clientKeys, self.serverData.encryptor, self.serverData.clientMessagesGot)

    def clientPublicKeyChange(self, key, clientId):
        #Import Key
        publicClientKey = RSA.importKey(key)
        self.serverData.clientKeys[clientId] = publicClientKey
        #Print Data
        message = "Got Client Key For: " + str(clientId) + " Public Key: " + str(publicClientKey)
        self.serverData.serverUiWindow.addToServerLogs(message)

    def packetNotFound(self, clientId):
        print("We Couldn't Find A Packet Function For: " + self.currentPacketData[0])