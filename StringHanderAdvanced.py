
def messageSpliter(timeBeforeSpace, textToSplit):
    #Making Counter
    currentLineCount = 0
    justMadeSpace = False
    #Setting Up Messages
    messages = textToSplit.split(" ")
    #End Message
    endMessage = ""

    for text in messages:
       #If \n Reset Count
       if(text == "\n" and justMadeSpace == False):
           endMessage += text
           currentLineCount = 0
           continue

       if(len(text) > timeBeforeSpace):
           messagesToAdd = []
           #While Text Is To Big Split
           while(len(text) > timeBeforeSpace):
               splitMessage = text[: timeBeforeSpace] + "-"

               messagesToAdd.append(splitMessage)
               text = text[timeBeforeSpace:]
           #Add To Message List
           messagesToAdd.append(text + " ")
           #Add To End Message
           for message in messagesToAdd:
               if(currentLineCount + len(message) > timeBeforeSpace):
                   endMessage += "\n"
                   currentLineCount = len(message)
               #Add To Message
               endMessage += message
               currentLineCount += len(message)
               #Made Space And Stop
               justMadeSpace = False
           continue

            #Check If It Will Go Past Max Message Count
       if(currentLineCount + len(text) > timeBeforeSpace):
           endMessage += " \n" + text + " "
           currentLineCount = len(text)
           #Made Space
           justMadeSpace = True
       else:
          if(text == ""):
              text = " "
              endMessage + text
          else:
              endMessage += text + " "
              #Add To Current Line Count
              currentLineCount += len(text)
              #Made Space 
              justMadeSpace = False

    return endMessage

def messageSpliterEncryption(timeBeforeSpace, textToSplit):
    #Making Counter
    currentLineCount = 0
    #Setting Up Messages
    messages = textToSplit.split(" ")
    #End Message
    endMessages = []
    currentMessage = ""

    for text in messages:
        if(len(text) > timeBeforeSpace):
            #While Text Is To Big Split
            messageToAdd = []
            while(len(text) > timeBeforeSpace):
                splitMessage = text[: timeBeforeSpace] + "-"

                messageToAdd.append(splitMessage)
                text = text[timeBeforeSpace:]
            #Add To Message List
            messageToAdd.append(text + " ")
            #Add To End Message
            for message in messageToAdd:
                if(currentLineCount + len(message) > timeBeforeSpace):
                    endMessages.append(currentMessage)
                    currentMessage = ""
                    currentLineCount = 0
                #Add To Message
                currentMessage += message
                currentLineCount += len(message)
            #Continue
            continue
        #Check If It Will Go Past Max Message Count
        if(currentLineCount + len(text) > timeBeforeSpace):
            endMessages.append(currentMessage)
            currentMessage = text + " "
            currentLineCount = len(text)
        else:
            if(text == ""):
                text = " "
                currentMessage += text
                currentLineCount += len(currentMessage)
            else:
                currentMessage += text + " "
                #Add To Current Line Count
                currentLineCount += len(text)
    endMessages.append(currentMessage)
    return endMessages

