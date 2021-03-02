import time
import math

charList = ["║", "■"]

def Blink(blinking_text, seconds, waitBlink = None, FinalMessage = None, type = None, Percentage = None):

    seconds = int(seconds)


    if(waitBlink == None):
        waitBlink = 0.2
    elif(waitBlink < 0.05):
        raise Exception("You can't put a blinking value lower than 0.1")

    while seconds > 0:
        print(blinking_text + "")
        

        time.sleep(waitBlink)
        seconds -= waitBlink
        print ("\033[A                             \033[A")
        print(blinking_text + ".  ")



        time.sleep(waitBlink)
        seconds -= waitBlink
        print ("\033[A                             \033[A")
        print(blinking_text + "..")


        time.sleep(waitBlink)
        seconds -= waitBlink
        print ("\033[A                             \033[A")
        print(blinking_text + "...")


        time.sleep(waitBlink)
        seconds -= waitBlink
        print ("\033[A                             \033[A")

    if FinalMessage != None:
        print(FinalMessage)

def Load_Bar(blinking_text = "", seconds = 0.5, FinalMessage = None, char = 0,type = None, Percentage = None, maxValue = 100):
    current_value = 1
    space_left = 0
    space_left = maxValue - current_value
    inser_val = maxValue - space_left

    while current_value < maxValue:
        print(f"{blinking_text} [", end="")
        while inser_val > 0:
            print(charList[char], end="")
            inser_val -= 1
        while space_left - 2 > 0:
            print(" ", end="")
            space_left -= 1
        print("]")
        space_left = maxValue - current_value
        inser_val = maxValue - space_left
        time.sleep(seconds)
        current_value += 1
        print ("\033[A                             \033[A")

    i = 0
    for i in range(200):
        print(" ", end="")
    print ("\033[A                             \033[A")
    if(FinalMessage != None):
        print(FinalMessage)



def Load(blinking_text, seconds, FinalMessage = None, char = None,type = None, maxValue = None, lastOne = None):
    cur_value = 0
    remain_value = 0
    i = 0
    if(maxValue == None):
        maxValue = 100
    if(maxValue < 1):
        raise Exception("You can't use a value that is lower than 1")

    seconds = seconds / maxValue

    char = int(char)

    if(char == None):
        cur_chac = charList[0]
    else:
        cur_chac = charList[char]

    #remain_value = maxValue - cur_value

    while cur_value < maxValue:
        percentage_val = cur_value / maxValue
        percentage_val = math.floor(percentage_val * 100)
        print(f"[" + blinking_text + "] - " + str(percentage_val) + "%")
        time.sleep(seconds)
        print ("\033[A                             \033[A")
        cur_value += 1
    if FinalMessage != None:
        if(lastOne == True):
            print(f"[" + blinking_text + "] - 100%")
        print(FinalMessage)