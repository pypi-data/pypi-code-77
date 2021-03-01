#=============#
#  PROPython  #
#=============#

#---------------#
# Version 1.0.0 #
#---------------#

# New version coming soon!

import random
import os
import pickle
import itertools
import time
import sys
import math

def PackageName():
    return cmd("<PROPython Package version: 1.0.0>")

def cmd(MESSAGE):
    print(MESSAGE)

def cmdColor(MESSAGE, colorID):
    print(colorID + MESSAGE)

def saveF(FILENAME, STRING):
    FILE = open(FILENAME, "w")
    FILE.write(STRING)
    FILE.close()

def deleteF(FILEPATH):
    os.remove(FILEPATH)

def cmdError(ERRORmessage):
    print("\033[31m" + ERRORmessage)

def createF(FILENAME):
    FILE = open(FILENAME, "w")
    FILE.write("")
    FILE.close()

def deleteAllFLines(FILENAME):
    FILE = open(FILENAME, "w")
    FILE.truncate()
    FILE.close()

def createArray(ARRAY):
    return ARRAY

def Upper(STRING):
    return STRING.upper()

def Lower(STRING):
    return STRING.lower()

def Return(returnWhat):
    return returnWhat

def FileDuplicate(FILENAME, NUMBERvalue):
    FILE = open(str(NUMBERvalue) + FILENAME, "w")
    FILE2 = open(FILENAME, "r")
    FILE.write(FILE2.read())
    FILE.close()
    FILE2.close()

def toStr(WHAT):
    return str(WHAT)

def toInt(WHAT):
    return int(WHAT)

def toFloat(WHAT):
    return float(WHAT)

def TimeToSleep(TIME):
    time.sleep(TIME)

def LoadingAnimation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def WritingAnimation(TEXT):
    for i in TEXT:
        time.sleep(0.3)
        print(i, end = '', flush = True)

def Round(NUMBER):
    return math.trunc(NUMBER)

def Floor(NUMBER):
    return math.floor(NUMBER)

def Ceil(NUMBER):
    return math.ceil(NUMBER)

def Enumerate(whatToEnum):
    for index, value in enumerate(whatToEnum):
        print("index: "+str(index)," value: "+str(value))

def ListLength(LIST):
    return len(LIST)

def computerSymbol(STRING):
    return ord(STRING)

def toDegree(FIRST, SECOND):
    return pow(FIRST, SECOND)

def SortDict(DICT):
    return sorted(DICT.items(), key=lambda item: (item[1], item[0]))

def toBinary(NUMBER):
    return bin(NUMBER)

def All(ITERABLE):
    return all(ITERABLE)

def Ascii(STRING):
    return math.ascii(STRING)

def summ(valuesL):
    res = 0

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res += x
        else:
            cmdError("Error! You have a string and you need int or float!")

    return res

def subtraction(valuesL):
    res = 0

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res = x - res
        else:
            cmdError("Error! You have a string and you need int or float!")

    return -res

def multiple(valuesL):
    res = 1

    for x in valuesL:
        if type(x) == int or type(x) == float:
            res = x * res
        else:
            cmdError("Error! You have a string and you need int or float!")

    return res

def division(valuesL):
    res = valuesL[0]

    if valuesL[0] == 0:
        cmdError("Error! Cannot be divided by zero!")

    for x in valuesL:
        if x == valuesL[0]:
            res = valuesL[0]
        else:
            if type(x) == int or type(x) == float:
                res = res / x
            else:
                cmdError("Error! You have a string and you need int or float!")

    return res

def NumberOfPi():
    return math.pi

def EulersNumber():
    return math.e

def Exponents(NUMBER):
    return math.exp(NUMBER)

def SquareRoot(NUMBER):
    return math.sqrt(NUMBER)

def IsPathExist(PATH):
    return os.path.exists(PATH)

def CreateDirictory(PATH):
    os.mkdir(PATH)

def DeleteDirectoryFile(PATH):
    os.remove(PATH)

def DeleteDicrectory(PATH):
    os.rmdir(PATH)

def GetFileSize(PATH):
    return os.path.getsize(PATH)

def FileRename(OLDNAME, NEWNAME):
    os.rename(OLDNAME, NEWNAME)

def FolderFilesList(PATH):
    return os.listdir(PATH)

def isInStringNumberOrLetter(STRING):
    return STRING.isalnum()

def isInStringNumber(STRING):
    return STRING.isnumeric()

def isInStringLetter(STRING):
    return STRING.isalpha()

def RandomNumber(START, STOP, STEP):
    return random.randrange(START, STOP, STEP)