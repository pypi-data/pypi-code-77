from . import splitLines




class StringWriter:
    """
    Write output stream to a string.
    """
    def __init__(self):
        self.text = ""


    def close(self):
        """
        Close output resource.
        """
        pass # Dummy, not used for StringWriter


    def flush(self):
        """
        Flush buffers.
        """
        pass # Dummy, not used for StringWriter


    def write (self, text_):
        """
        Write text.
        """
        self.text = self.text + str (text_)




class FileWriter:
    """
    Write output stream to a file
    """
    def __init__(self, fileName: str, fileMode: str = "w"):
        self.fileName = fileName
        self.fileMode = fileMode
        self.file = open (fileName, fileMode)


    def close(self):
        if self.file != None:
            self.file.close ()
            self.file = None


    def flush(self):
        if self.file != None:
            self.file.flush ()

    
    def write(self, text_):
        assert self.file != None, "File must not be closed when writing text."
        self.file.write (text_)
    



class TextWriter:
    """
    Used to write structured text to a StreamWriter.
    """
    def __init__(self, writer: object, indentSize: int = 4):
        self.writer = writer
        self.indentSize = indentSize
        self.indent = 0
        self.indentOnLineBegin = None
        self.buffer = ""


    def close (self):
        """
        Closes the StreamWriter behind this TextWriter.
        """
        self.flush ()
        self.writer.close ()
        self.writer = None


    def formatNumber (self, number: float) -> str:
        """
        Formats a number.
        """
        return str (number)


    def writeNumber (self, number: float):
        """
        Write a number.
        """
        return self.write (self.formatNumber (number))


    def write (self, text: str) -> None:
        """
        Write some text.
        """
        if self.indentOnLineBegin == None:
            self.indentOnLineBegin = self.indent
        lines = splitLines (str (text))
        if (len (lines) > 0):
            self.buffer = self.buffer + lines[0]
        if (len (lines) > 1):
            self.flush ()
        for index in range (1, len (lines) - 1):
            self.buffer = lines[index]
            self.flush ()
        if (len (lines) > 1):
            self.buffer = self.buffer + lines[len (lines) - 1]


    def flush (self):
        """
        flushes the current text buffer to the file
        """
        if (self.buffer != ""):
            if self.indentOnLineBegin == None:
                self.indentOnLineBegin = self.indent
            self.writer.write (" " * (self.indentOnLineBegin * self.indentSize))    
            self.writer.write (self.buffer + "\n")
        self.indentOnLineBegin = None
        self.buffer = ""


    def increaseIndent (self) -> None:
        """
        Increase identation used for next write call
        """
        self.indent = self.indent + 1


    def decreaseIndent (self) -> None:
        """
        """
        assert self.indent > 0, "Indentation error"
        self.indent = self.indent - 1


    def __lineEmpty(self):
        """
        Returns true if the current line is empty
        """
        return self.buffer == ""
