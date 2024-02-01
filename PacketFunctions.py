import StringHanderAdvanced as stringFunctions

def splitPacketMessageClient(packet, maxMessageLength):
    #Packets
    packetsToSend = []
    #Messages
    message = packet[1]
    #Split Message
    messages = stringFunctions.messageSpliterEncryption(maxMessageLength, message)

    for message in messages:
        packetToSend = [packet[0], message]
        packetsToSend.append(packetToSend)

    return packetsToSend

