import PacketFunctions as functions

class ServerSend:
    #Connections
    connections = []
    connectionsUDP = []
    clientIds = []
    #TCP
    packetQueueTCP = []
    writingPacketTCP = False
    #UDP
    writingPacketUDP = False
    packetQueueUDP = []

    def sendPacket(self, packet, connection, currentState):
        self.writingPacketTCP = True
        if(currentState == True):
            self.packetQueueTCP.append((packet, connection))
            print("writing packet")
            return

        #Send Packet
        connection.transport.write(packet)
        #Run Function If Queue
        if(len(self.packetQueueTCP) >= 1):
            # 0 = packet
            # 1 = Connection
            packet = self.packetQueueTCP[0]
            self.packetQueueTCP.pop(0)
            self.sendPacket(packet[0], packet[1], False)
        else:
            self.writingPacketTCP = False

    def sendPacketUDP(self, packet, connection, currentState):
        self.writingPacketUDP = True
        if(currentState == True):
            self.packetQueueUDP.append((packet, connection))
            print("writing packet")
            return

        #Send Packet
        connection.transport.write(packet, connection.address)
        #Run Function If Queue
        if(len(self.packetQueueUDP) >= 1):
            # 0 = packet
            # 1 = Connection
            packet = self.packetQueueUDP[0]
            self.packetQueueUDP.pop(0)
            self.sendPacket(packet[0], packet[1], False)
        else:
            self.writingPacketUDP = False

    def updateServerInfo(self, connectionList, clientIds):
        print("Connection List Changed")
        self.connections = connectionList
        self.clientIds = clientIds

    def welcome(self, message, clientId, udpPort, keys, encryptor, clientMessagesGot):
        #Main Packets
        packetForOldClients = ["welcome", "Server: " + "Some Else Is Here!"]
        #Split Packets
        packetForOldClientsSplit = functions.splitPacketMessageClient(packetForOldClients, 10)
        for id in self.clientIds:
            if(id == clientId):
                packet = ["welcomeMe", "Server: " + message, clientId, udpPort]
                #Sending Packets
                encryptedPacket = encryptor.encryptUsingPublicKey(packet, keys[id])
                self.sendPacket(encryptedPacket, self.connections[id][0], self.writingPacketTCP)

                clientMessagesGot[id] += 1
            else:
                #Sending Packets
                for packet in packetForOldClientsSplit:
                    #Adding Needed Part
                    packet.append(clientMessagesGot[id])
                    #Sending Packet
                    encryptedPacket = encryptor.encryptUsingPublicKey(packet, keys[id])
                    self.sendPacket(encryptedPacket, self.connections[id][0], self.writingPacketTCP)

                    clientMessagesGot[id] += 1

    def sendMessage(self, packet, UDPConnection):
        self.sendPacketUDP(packet, UDPConnection, self.writingPacketUDP)

    def changeClientIds(self, keys, encryptor):
        for id in self.clientIds:
            packetContent = ["forceDisconnect", "Id Changing We Will Get You Back In Soon!"]
            encryptedPacket = encryptor.encryptUsingPublicKey(packetContent, keys[id])
            self.sendPacket(encryptedPacket, self.connections[id][0], self.writingPacketTCP)

    #Keys
    def sendPublicKey(self, key, clientId):
        packet = bytes("serverPublicKey ", 'utf-8') + key
        print("sending key to: " + str(clientId))
        self.sendPacket(packet, self.connections[clientId][0], self.writingPacketTCP)

    def serverChangePublicKey(self, key):
        for id in self.clientIds:
            packet = bytes("serverPublicKeyChange ", 'utf-8') + key
            self.sendPacket(packet, self.connections[id][0], self.writingPacketTCP)