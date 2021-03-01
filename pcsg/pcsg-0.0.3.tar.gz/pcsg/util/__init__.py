from . import hash as hashUtil


def hash(*arguments):
    """
    Calculates a hash code for a list of arguments with arbirtary types, returns an unsigned 64 bit number.
    """
    value = ""
    for a in arguments:
        value = value + str (hashUtil._hashArgument (a)) + ","
    return hashUtil._hashString (value)




def splitLines (text: str) -> list:
    """
    Split string into single lines, retaining also empty ones.
    """
    lastEntry = 0
    elements = []
    strLen = len (text)
    for i in range (0, strLen):
        if text[i] == "\n":
            elements.append (text[lastEntry : i])
            lastEntry = i + 1
    if len (text) >= lastEntry:
        elements.append (text[lastEntry : len (text)])
    return elements




def breakLines (text, maxWidth, maxWidthFirst = None):
    """
    Breaks a line into multiple lines.
    """
    if maxWidthFirst == None:
        maxWidthFirst = maxWidth
    mw = maxWidthFirst
    result = []
    for l in splitLines (text):
        temp = l
        while len (temp) > mw:
            pos = _breakLineSplitPos (temp, mw)
            result.append (temp[0 : pos])
            if pos < len (temp):
                if temp[pos] == " " or temp[pos] == "\n" or temp[pos] == "\t":
                    pos = pos + 1
                temp = temp [pos : len (temp)]
            else:
                temp = ""
            mw = maxWidth
        result.append (temp)
    return result





def _breakLineSplitPos (text, maxWidth):
    """
    Get position for text splitting.
    """
    if len (text) < maxWidth:
        return len (text)
    lastSplitPos = None
    for i in range (1, len (text)):
        if text[i] == " " or text[i] == "\t" or text[i] == "\n":
            if (i >= maxWidth):
                if lastSplitPos == None:
                    return maxWidth
                else:
                    return lastSplitPos
            lastSplitPos = i
    if lastSplitPos == None:
        return maxWidth
    else:
        return lastSplitPos





def formatTableEntryLeftSize (left, width, leftSize, centerSpace = 2, indent = 2):
    """
    Get size of left column after formatting table entry.
    """
    lbs = leftSize + centerSpace
    if (lbs + 2) > width:
        width = (lbs + 2)
    leftSplit = breakLines (left, leftSize - indent, leftSize)
    maxLineSize = 0
    for i in range (0, len (leftSplit)):
        lt = leftSplit[i]
        if i > 0:
            lt = (" " * indent) + lt
        if len (lt) > maxLineSize:
            maxLineSize = len (lt)
    return maxLineSize





def formatTextBlock (text, indent = 2, maxLineSize = None, prefix: str = ""):
    """
    Format block of Text.
    """
    mls = 1000
    if maxLineSize != None:
        mls = maxLineSize
    breakSizeFirst = mls - len (prefix)
    breakSize = breakSizeFirst - indent
    splited = breakLines (text, breakSize, breakSizeFirst)
    indentStr = " " * indent
    buffer = ""
    for line in splited:
        if buffer == "":
            buffer = prefix + line
        else:
            buffer = buffer + "\n" + indentStr + prefix + line
    return buffer




def formatTableEntry (left, right, width = 80, leftSize = 30, centerSpace = 2, indent = 2, prefix = ""):
    """
    Format table entry.
    """
    lbs = len (prefix) + leftSize + centerSpace
    if (lbs + 2) > width:
        width = (lbs + 2)
    rbs = width - lbs
    leftSplit = breakLines (left, leftSize - indent, leftSize)
    rightSplit = breakLines (right, rbs - indent, rbs)
    while len (leftSplit) < len (rightSplit):
        leftSplit.append ("")
    while len (leftSplit) > len (rightSplit):
        rightSplit.append ("")
    buffer = ""
    for i in range (0, len (leftSplit)):
        lt = leftSplit[i]
        rt = rightSplit[i]
        if i > 0:
            lt = (" " * indent) + lt
            rt = (" " * indent) + rt
        pads = lbs - len (lt)
        if (pads > 0):
            out = lt + " " * pads + rt
        else:
            out = lt + rt
        if buffer != "":
            buffer = buffer + "\n"
        buffer = buffer + prefix + out
    return buffer