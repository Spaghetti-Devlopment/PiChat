import json
#For Encription Stuff
from Cryptodome.Cipher import AES;
from Cryptodome import Random;
#Public Private Key
from Cryptodome.Cipher import PKCS1_OAEP;
from Cryptodome.PublicKey import RSA;
#String Formating
import StringHanderAdvanced as stringFunctions

#Encryptor
class Encryptor:
    #Keys
    privateKey = set
    backupKey = set
    publicKey = set
    publicKeyString = ""
    #Everything Else
    IV = set
    isMakingNewKeys = False;

    def __init__(self):
        #Making Keys
        key = RSA.generate(2048)
        #Server Key
        self.privateKey = key
        #Public Key
        self.publicKey = key.public_key()
        self.publicKeyString = self.publicKey.exportKey(format='PEM')
        #Print Key Info
        print("Current Public Key: " + str(self.publicKey) + "\nCurrent Private Key: " + str(self.privateKey) + "\n")

    #Key Changing
    def changeKeys(self):
        self.isMakingNewKeys = True
        #Making Keys
        key = RSA.generate(2048)
        #Server Key
        self.backupKey = self.privateKey
        self.privateKey = key
        #Public Key
        self.publicKey = key.public_key()
        self.publicKeyString = self.publicKey.exportKey(format='PEM')
        #Print Key Info
        print("New Public Key: " + str(self.publicKey) + "\nNew Private Key: " + str(self.privateKey) + "\n")
        self.isMakingNewKeys = False

    #Encrypting
    def encryptUsingPublicKey(self, jsonData, key):
        publicCipher = PKCS1_OAEP.new(key)
        packet = json.dumps(jsonData)
        encryptedPacket = publicCipher.encrypt(bytes(packet, 'utf-8'))
        return encryptedPacket

    def decryptPrivateKey(self, data):
        if(self.isMakingNewKeys == True):
            print("Making New Keys")

        try:
            privateCipher = PKCS1_OAEP.new(self.privateKey)
            packet = privateCipher.decrypt(data)
            packet = json.loads(packet)
            return packet
        except:
            print("New Key Failed Trying Old Key...")
            privateCipher = PKCS1_OAEP.new(self.backupKey)
            packet = privateCipher.decrypt(data)
            packet = json.loads(packet)
            return packet
