import json
from tkinter import END
import PacketFunctions as functions
from time import sleep

class clientSend:
    #Messaging
    messageQueue = []
    sendingMessage = False
    #Packet Sending
    #TCP
    packetQueueTCP = []
    writingPacketTCP = False
    #UDP
    writingPacketUDP = False
    packetQueueUDP = []

    def sendPacketTCP(self, packet, client, currentState):
        self.writingPacketTCP = True
        if(currentState == True):
            self.packetQueueTCP.append((packet, client))
            print("writing packet")
            return

        #Send Packet
        client.transport.write(packet)
        #Run Function If Queue
        if(len(self.packetQueueTCP) >= 1):
            # 0 = packet
            # 1 = Connection
            packet = self.packetQueueTCP[0]
            self.packetQueueTCP.pop(0)
            self.sendPacketTCP(packet[0], packet[1], False)
        else:
            self.writingPacketTCP = False

    def sendPacketUDP(self, packet, udpServer, currentState):
        self.writingPacketUDP = True
        if(currentState == True):
            self.packetQueueUDP.append((packet, udpServer))
            print("writing packet")
            return

        #Send Packet
        udpServer.transport.write(packet)
        #Run Function If Queue
        if(len(self.packetQueueUDP) >= 1):
            # 0 = packet
            # 1 = Connection
            packet = self.packetQueueUDP[0]
            self.packetQueueUDP.pop(0)
            self.sendPacketTCP(packet[0], packet[1], False)
        else:
            self.writingPacketUDP = False

    #Main Message System
    def sendMessage(self, inputText, client):
        #Formating Message
        message = inputText.get("1.0", END)

        message = message.replace("\n", "*")

        #Make Sure Message Isn't Just A Space
        if(message == " " or message == ""):
            return

        #Remove All Spaces At The Start
        for letter in message:
            if(letter == " "):
                message = message.replace(" ", "", 1)
            else:
                break
        #Sending Message
        #Check If Changing Keys
        if(client.changingKeys or self.sendingMessage == True):
            self.messageQueue.append(message)
            inputText.delete("1.0", END)
            print("Adding To Message Queue: " + str(self.messageQueue))
            client.chat.sendingMessage(len(self.messageQueue))
            return

        self.sendingMessage = True
        #Send Message
        packetContent = ["message", client.username + ": " + message]
        packetsToSend = functions.splitPacketMessageClient(packetContent, 100)
        inputText.delete("1.0", END)
        for packet in packetsToSend:
            encryptedPacket = client.encryptor.encryptUsingPublicKey(packet, client.serverPublicKey)
            self.sendPacketUDP(encryptedPacket, client.udpServer, self.writingPacketUDP)
        #Queue
        if(len(self.messageQueue) >= 1):
            message = self.messageQueue[0]
            self.messageQueue.pop(0)
            self.sendMessageQueue(message, client)
        else:
            self.sendingMessage = False

    def sendMessageQueue(self, message, client):
        #Check If Changing Keys
        if(client.changingKeys):
            self.messageQueue.append(message)
            client.chat.sendingMessage(len(self.messageQueue))
            return

        #Send Message
        packetContent = ["message", client.username + ": " + message]
        packetsToSend = functions.splitPacketMessageClient(packetContent, 100)
        for packet in packetsToSend:
            encryptedPacket = client.encryptor.encryptUsingPublicKey(packet, client.serverPublicKey)
            self.sendPacketUDP(encryptedPacket, client.udpServer, self.writingPacketUDP)
            #Remove From Queue
            client.chat.sendingMessage(len(self.messageQueue))

    def messageQueueClear(self, client):
        for message in self.messageQueue:
            self.sendMessageQueue(message, client)
        #Reset Queue
        self.messageQueue = []

        client.chat.sendingMessage(len(self.messageQueue))

    def askForId(self, client):
        packetContent = ["idRequest"]
        jsonPacket = json.dumps(packetContent)
        client.transport.write(bytes(jsonPacket, 'utf-8'))

    def askForKey(self, client):
        packetContent = ["serverKeyRequest"]
        jsonPacket = json.dumps(packetContent)
        client.transport.write(bytes(jsonPacket, 'utf-8'))

    def sendPublicKeyFirst(self, key, client):
        print(key)
        packet = bytes("clientPublicKeyFirst ", 'utf-8') + key
        self.sendPacketTCP(packet, client, self.writingPacketTCP)

    def clientPublicKeyChange(self, key, client):
        packet = bytes("clientPublicKeyChange ", 'utf-8') + key
        self.sendPacketTCP(packet, client, self.writingPacketTCP)
        client.changingKeys = False
        self.messageQueueClear(client)


