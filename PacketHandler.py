import json
import threading
from Cryptodome.PublicKey import RSA
#Ui
from UI import chatWindow

class PacketHandlerClient:

    client = set
    clientUi = set

    def __init__(self, client):
        print("Packet Handler Setup Started")
        print(self.clientUi)
        self.client = client
        #UI
        uiThread = threading.Thread(target=chatWindow, args=(self.client,))
        uiThread.daemon = True
        uiThread.start()

    def packetData(self, packetData):
        self.clientUi = self.client.chat
        if(self.checkIfJson(packetData) == True):
            #Getting Function
            packetName = packetData[0]
            #Getting Function
            function = getattr(self, packetName, lambda: self.packetNotFound(packetName))
            function(packetData)
        else:
            print("Decoding Key")
            #This is ONLY Used For Getting Keys <:(
            #Decoding
            try:
                print(packetData)
                decodedData = bytes.decode(packetData, 'utf-8')
                commandKey = decodedData.split(' ', 1)
                #Getting Packet Name
                packetName = commandKey[0]
                #Getting Function
                function = getattr(self, packetName, lambda: self.packetNotFound(packetName))
                function(commandKey[1])
            except Exception as e:
                print("Cannot Process Packet: " + str(e))

    #Check If Json
    def checkIfJson(self, file):
        try:
            file = json.dumps(file)
            json.loads(file)
            print("File Is Json")
            return True
        except:
            return False

    #Packet Handleing
    def welcomeMe(self, packet):
        #Return If Been Welcomed
        if(self.client.hasBeenWelcomed):
            return

        #Get Message
        message = packet[1]
        #Add To Message List
        self.client.messages.insert(1, message)
        print(self.client.messages)
        #Setup ID and Message
        self.client.clientId = packet[2]
        self.clientUi.addToMessageList(1, self.client, False)
        self.client.hasBeenWelcomed = True
        #UDP Port
        self.client.udpPort = packet[3]
        print(packet[3])
        #Start UDP
        self.client.startUDP()

    def welcome(self, packet):
        message = packet[1]
        index = packet[2]
        print("Someone Else Is Here!")
        self.client.messages.insert(index, message)
        self.clientUi.addToMessageList(index, self.client, False)

    def message(self, packet):
        #Message
        print(packet)
        message = packet[1]
        message = message.replace("*", " \n ")
        #Indexing
        index = packet[2]
        replaceLastMessage = packet[3]
        #Adding To Message List
        self.client.messages.insert(index, message)
        self.clientUi.addToMessageList(index, self.client, replaceLastMessage)

    def forceDisconnect(self, packet):
        message = "You Where Made To Disconnect: " + packet[1]
        print(message)
        self.client.connected = False
        self.client.clientSend.reconnectSetup(self.client)

    #Keys
    def serverPublicKey(self, key):
        print("Getting Public Key...")
        #Import Key
        publicServerKey = RSA.importKey(key)
        self.client.serverPublicKey = publicServerKey
        #Print Info
        print("Got Server Public Key: " + str(publicServerKey))
        self.client.clientSend.sendPublicKeyFirst(self.client.encryptor.publicKeyString, self.client)

    def serverPublicKeyChange(self, key):
        self.client.changingKeys = True
        print("Getting New Public Key...")
        #Import Key
        publicServerKey = RSA.importKey(key)
        self.client.serverPublicKey = publicServerKey
        #Print Info
        print("Got Server New Public Key: " + str(publicServerKey))
        self.client.encryptor.changeKeys()
        self.client.clientSend.clientPublicKeyChange(self.client.encryptor.publicKeyString, self.client)

    def packetNotFound(self, packetName):
        print("We Couldn't Find A Packet Function For: " + packetName)