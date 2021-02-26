
## Basic Operations 
def add(a,b): 
    return a+b 

def subtract(a,b): 
    return a-b 

def multiply(a,b):
    return a*b

def divide(a,b): 
    return a/b

def divideInt(a,b):
    return a//b 

def mod(a,b):
    return a%b 

def exponent(a,b): 
    return a**b 

## More specific stuff
def GCD(a,b):
    bigVal , smallVal = max([a,b]) , min([a,b])
    # start euclid's alogirthm 

    done = False 
    while not done:

        tempVal = bigVal 
        bigVal = smallVal    
        potentialGCD = smallVal 
        smallVal = tempVal % smallVal
        if smallVal ==0: 
            return potentialGCD

def gcdSteps(a,b):
    def equationFormat(valOne, valTwo, valThree, valFour):
        return "{} = {}*{} + {}".format(valOne, valTwo, valThree, valFour)

    def endingsFormat(valOne, valTwo, valThree, valFour): 
        return "{} = {} - {}*{}".format(valFour, valOne, valTwo, valThree)
    
    def popEndValue(list):
        return list[0:len(list)-1]

    endingVals = []    
    allEquations=[]
    bigVal , smallVal = max([a,b]) , min([a,b])
    # start euclid's alogirthm  
    # FORMAT =>  A = M*X + B  
    aValues =[]
    mValues =[]
    xValues =[]
    bValues =[]

    done = False 
    while not done:
        
        tempVal = bigVal 
        bigVal = smallVal    
        smallVal = tempVal % smallVal
        endingVals.append(endingsFormat(tempVal,bigVal,tempVal//bigVal,smallVal))
        allEquations.append(equationFormat(tempVal,bigVal,tempVal//bigVal,smallVal))

        aValues.append(tempVal)
        mValues.append(bigVal)
        xValues.append(tempVal//bigVal)
        bValues.append(smallVal)

        if smallVal ==0: 
            break 
    aValues = popEndValue(aValues)
    mValues = popEndValue(mValues)
    xValues = popEndValue(xValues)
    bValues = popEndValue(bValues)
    endingVals = popEndValue(endingVals)

    # print("\n",aValues,"\n",mValues,"\n", xValues,"\n" , bValues, "\n")
    
    return allEquations, endingVals


def simplifyCongruence(initVal1, initVal2, iterVal): 
    returnVals = []
    while initVal1 <0: 
        initVal1+=iterVal 
        if initVal1>0: 
            returnVals.append(initVal1)
            break 

    while initVal1-iterVal> 0: 
        initVal1 -= iterVal
        if initVal1-iterVal < 0:
            returnVals.append(initVal1)
            break 

    while initVal2 <0: 
        initVal2+=iterVal 
        if initVal2>0: 
            returnVals.append(initVal2)
            break 

    while initVal2-iterVal> 0: 
        initVal2 -= iterVal
        if initVal2-iterVal < 0:
            returnVals.append(initVal2)
            break 
    
    
    templateFormat = "\n\n {} ≊ {} (mod {})\n\n".format(initVal1, initVal2, iterVal)
    return templateFormat

def linearCombination(valueOne, valueTwo): 
    gcdValue = GCD(valueOne,valueTwo)
    equation = "{} = {} + {}".format(gcdValue,valueOne,valueTwo)

    equation= equation.split("=")
    
    return equation