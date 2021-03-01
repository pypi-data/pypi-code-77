import math
import sys
import copy
import os
import re
from . import formatTextBlock
from . import formatTableEntry
from . import formatTableEntryLeftSize




class Option:
    """
    The base class of Flags and Parameters.
    """
    def __init__(self, 
                    name: str,
                    short: str,
                    description: str,
                    default,
                    group,
                    filterFunc
        ):

        #: Name of the Option (required for displaying help).
        self.name = name

        #: Short identifier string (a single char).
        self.short = short

        #: Description of the Option (required for displaying help).
        self.description = description

        #: Group name (required for displaying help).
        self.group = group

        #: Default value for optional Options.
        self.default = default

        #: Value after parsing the commandline.
        self.value = default

        #: Filter function to check parsed values.
        #: def filter (Option, Value) -> str: Function shall return an error string for bad arguments, None if accepted.
        self.filterFunc = filterFunc

        # Internal flag for parser: Option has been parsed
        self.parsed = False




class Flag(Option):
    """
    Flag for command line parser. A flag is simply a boolean flag which is parsed from a command line argument in form **\-\-name** or **\-s(hort)**.
    """
    def __init__(self, name: str, short: str, description: str, group: str, filterFunc = None):
        super().__init__(name, short, description, False, group, filterFunc)


    def onParse(self, parser, value):
        filterResult = None
        if self.filterFunc != None:
            filterResult = self.filterFunc (self, value)
        if filterResult != None:
            return filterResult
        self.parsed = True
        self.value = True
        return None




class Parameter(Option):
    """
    Parameter for command line parser. A parameter is a data value parsed from a command line argument in form **\-\-name value** or **\-s(hort) value**.
    """
    def __init__(self, name: str, short: str, description: str, group: str, default = None, valueName = None, filterFunc = None):
        super().__init__(name, short, description, default, group, filterFunc)

        #: Name of value (required for displaying help).
        self.valueName = valueName


    def onParse(self, parser, value):
        filterResult = None
        if self.filterFunc != None:
            filterResult = self.filterFunc (self, value)
        if filterResult != None:
            return filterResult
        self.parsed = True
        self.value = value
        return None




class ParameterChoose(Parameter):
    """
    Like Parameter, but the choosable options are fixed by a list.
    """
    def __init__(self, name: str, short: str, description: str, group: str, items: dict, default = None, valueName = None, filterFunc = None):
        super().__init__(name, short, description, group, default, valueName, filterFunc)

        #: Name of value (required for displaying help).
        self.valueName = valueName

        #: A dictionary containing the chooseable items. The key is the option string for the command line. Value should contain a dict {'description': aString} for displaying the help.
        self.items = items


    def onParse(self, parser, value):
        if self.filterFunc != None:
            return self.onParse (parser, value)
        if not value in self.items:
            return "has no option \'" + value + "\'"
        self.parsed = True
        self.value = value
        return None




class Argument:
    """
    Argument for command line parser. Arguments get parsed in the order the are registered at the Parser.
    """
    def __init__(self, 
                    name: str, 
                    description: str, 
                    isOptional: bool = False, 
                    optionalParsing: bool = False, 
                    default = None, 
                    isArray: bool = False, 
                    filterFunc = None
                ):

        #: Name of the Argument (required for displaying help).
        self.name = name

        #: Description of the Argument (required for displaying help).
        self.description = description

        #: If True, the Argument is displayed as optional (required for displaying help).
        self.isOptional = isOptional

        #: If True, the Argument is parsed as optional (required for parsing).
        self.optionalParsing = optionalParsing

        #: The Argument is parsed as array and can be used multiple times.
        self.isArray = isArray

        #: Default value for optional Argument.
        self.default = default

        #: Value after parsing the commandline.
        self.value = default

        #: Filter function to check parsed values.
        #: def filter (Option, Value) -> str: Function shall return an error string for bad arguments, None if accepted.
        self.filterFunc = filterFunc

        # Internal flag for parser: Argument has been parsed
        self.parsed = False


    def onParse(self, parser, value):
        filterResult = None
        if self.filterFunc != None:
            filterResult = self.filterFunc (self, value)
        if filterResult != None:
            return filterResult
        self.parsed = True
        self.value = value
        return None




class ArgumentChoose(Argument):
    """
    Like Argument, but the choosable options are fixed by a list.
    """
    def __init__(self, name, description, items: dict, isOptional = False, optionalParsing = False, default = None, isArray = False, filterFunc = None):
        super().__init__(name, description, isOptional = isOptional, optionalParsing = optionalParsing, default = default, isArray = isArray, filterFunc = filterFunc)
        self.items = items


    def onParse(self, parser, value):
        if self.filterFunc != None:
            return self.onParse (parser, value)
        if not value in self.items:
            return "has no option \'" + value + "\'"
        self.parsed = True
        self.value = value
        return None




class ExtraArguments:
    """
    ExtraArguments takes all extra command line arguments after **\-\-** was parsed. Arguments **\-\-** are not interpreted by the Parser.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.value = []
        self.parsed = False


    def onParse(self, parser, value):
        self.parsed = True
        self.value = value
        return None




def FilterNumber(param, value):
    """
    Filter: Assert number.
    """
    if re.match(r'^-?\d+(?:\.\d+)?$', value) is None:
        return "parameter --" + param.name + " expectes a number as value"
    return None




def FilterNumberGreterZero(param, value):
    """
    Filter: Assert number greater than zero.
    """
    if re.match(r'^-?\d+(?:\.\d+)?$', value) is None:
        return "parameter --" + param.name + " expectes a number as value"
    if float (value) <= 0:
        return "parameter --" + param.name + " expectes a number greater zero"
    return None




def FilterInteger(param, value):
    """
    Filter: Assert integral number.
    """
    if value.isnumeric () == False:
        return "parameter --" + param.name + " expectes an integer as value"
    return None




def FilterIntegerGreterZero(param, value):
    """
    Filter: Assert integral number greater than zero.
    """
    if value.isnumeric () == False:
        return "parameter --" + param.name + " expectes an integer as value"
    if int (value) <= 0:
        return "parameter --" + param.name + " expectes an integer greater zero"
    return None




class Parser:
    """
    Parser for command line with integrated help system.
    """
    def __init__(self, title = None, description = None):
        self.title = title
        self.description = description
        self.entries = []
        self.indent = 2
        self.centerSpace = self.indent
        # TODO: get line size on runtime
        self.defaultLineSize = 80
        

    def register(self, entry):
        """
        Register flag, parameter or argument.
        """
        hasArray = False
        hasOptional = False
        hasExtraArgs = False
        for e in self.entries:
            if isinstance (e, ExtraArguments):
                hasExtraArgs = True
            if isinstance (e, Argument):
                if e.isOptional:
                    hasOptional = True
                if e.isArray:
                    hasArray = True
        if isinstance (entry, (Flag, Parameter)):
            for e in self.entries:
                if isinstance (e, (Flag, Parameter, ParameterChoose)):
                    if e.name == entry.name:
                        assert False, "an option with name --" + str (e.name) + " already exists." 
                    if ((entry.short != None) and (e.short == entry.short)):
                        assert False, "an option with name -" + str (e.short) + " already exists." 
            self.entries.append (entry)
        elif isinstance (entry, Argument):
            if hasArray:
                assert False, "can not add an argument after an array of arguments"
            if hasOptional:
                if entry.isOptional == False:
                    assert False, "can not add a non-optional argument after an optional argument"
            self.entries.append (entry)
        elif isinstance (entry, ExtraArguments):
            assert hasExtraArgs == False, "can not add ExtraArguments twice."
            self.entries.append (entry)
        else:
            assert False, "type of entry is invalid"


    def showHelp(self, withDescription = True):
        """
        Show command line help.
        """
        # Short title
        appName = ""
        if len (sys.argv) > 0:
            appName = str (sys.argv[0])
        if self.title != None:
            print (appName + " - " + self.title)
        else:
            print (appName)
        
        # Usage
        print ("\nusage: " + appName + " " + self._formatUsage ())

        # Description
        if withDescription and (self.description != None):
            print ("\n" + self.description)

        # Calculate table sizes
        lineSize = self.defaultLineSize
        minLineSize = 40
        if lineSize < minLineSize:
            lineSize = minLineSize

        # Table formatting
        indent = self.indent
        centerSpace = self.centerSpace - 1
        if centerSpace < 0:
            centerSpace = 0
        leftColSize = math.floor (lineSize * 0.4)
        minLineSize = leftColSize + centerSpace + 10 + indent
        if lineSize < minLineSize:
            lineSize = minLineSize

        # determine size of left column
        minLeftSize = 0
        for entry in self.entries:
            if isinstance (entry, Argument):
                if (len (entry.name) > minLeftSize):
                    minLeftSize = len (entry.name)
        for entry in self.entries:
            if isinstance (entry, (Flag, Parameter)):
                l, r = self._formatOption (entry, indent, 1000)
                ls = formatTableEntryLeftSize (l, lineSize, leftColSize, centerSpace, indent = indent) + indent
                if (ls > minLeftSize):
                    minLeftSize = ls
        minLeftSize = minLeftSize
        if minLeftSize < leftColSize:
            leftColSize = minLeftSize
        if leftColSize < 10:
            leftColSize = 10

        leftColSize = leftColSize - indent

        # maximum right table size
        maxRightSize = lineSize - centerSpace - leftColSize - indent

        # Command line arguments
        first = True
        for entry in self.entries:
            if isinstance (entry, Argument):
                if first:
                    print ("\nArguments:")
                    first = False
                l = entry.name
                r = entry.description
                if isinstance (entry, ArgumentChoose):
                    astr = self._formatChooseables (entry, "", indent, maxRightSize)
                    if astr != "":
                        astr = "\n" + astr
                    r = r + astr
                if entry.default != None:
                    if r != "":
                        r = r + "\n"
                    r = r + "Default value: " + str (entry.default)
                s = formatTableEntry (l, r, lineSize, leftColSize, centerSpace, indent = indent, prefix = " " * indent)
                print (s)
        for entry in self.entries:
            if isinstance (entry, ExtraArguments):
                if first:
                    print ("\nArguments:")
                    first = False
                l = "-- " + entry.name
                r = entry.description
                s = formatTableEntry (l, r, lineSize, leftColSize, centerSpace, indent = indent, prefix = " " * indent)
                print (s)

        # Command line flags and options
        groups = {}
        groupOrder = []
        for entry in self.entries:
            if isinstance (entry, (Flag, Parameter)):
                if entry.group in groups:
                    groups[entry.group].append (entry)
                else:
                    groups[entry.group] = [entry]
                    groupOrder.append (entry.group)
        for groupName in groupOrder:
            first = True
            for entry in groups[groupName]:
                if first:
                    print ("\n" + groupName + ":")
                    first = False
                l, r = self._formatOption (entry, indent, maxRightSize)
                s = formatTableEntry (l, r, lineSize, leftColSize, centerSpace, indent = indent, prefix = " " * indent)
                print (s)


    def _formatUsage(self):
        """
        Format usage for displaying help.
        """
        text = ""
        for entry in self.entries:
            if isinstance (entry, (Parameter, Flag)):
                text = "[--<options> ...]"
                break
        for entry in self.entries:
            if isinstance (entry, Argument):
                if text != "":
                    text = text + " "
                en = entry.name
                if entry.isArray:
                    en = en + " ..."
                if entry.isOptional:
                    en = "[" + en + "]"
                text = text + en
        for entry in self.entries:
            if isinstance (entry, ExtraArguments):
                if text != "":
                    text = text + " "
                text = text + " [-- " + entry.name + " ...]"
        return text


    def _formatOption(self, option, indent, maxRightSize):
        """
        Format an option for displaying help.
        """
        text = "--" + option.name
        if option.short != None:
            if option.short != "":
                text = text + ", -" + option.short
        if isinstance(option, Parameter):
            text = text + " $" + option.valueName
        desc = ""
        if option.description != None:
            desc = option.description
        desc = self._formatChooseables (option, desc, indent, maxRightSize)
        if isinstance (option, Parameter):
            if option.default != None:
                if desc != None:
                    desc = desc + "\n"
                desc = desc + "Default value: " + str (option.default)
        return (text, desc)


    def _formatChooseables(self, entry, oldText, indent, maxRightSize):
        """
        Format choosable options.
        """
        newText = oldText
        if not isinstance (entry, (ParameterChoose, ArgumentChoose)):
            return oldText
        emitNewLine = False
        if newText != "":
            emitNewLine = True
        for key in entry.items:
            ostr = "\'" + key + "\'"
            mi = entry.items[key]
            if "description" in mi:
                descr = mi["description"]
                if descr != None:
                    if descr != "":
                        idescr = formatTextBlock (descr, indent, maxRightSize - indent)
                        ostr = ostr + ":\n" + idescr
            if emitNewLine:
                newText = newText + "\n"    
            newText = newText + formatTextBlock (ostr, indent, maxRightSize - indent)
            emitNewLine = True
        return newText


    def commandlineInvalid(self, message):
        """
        Print error and terminate application with error code 1.
        """
        appName = ""
        if len (sys.argv) > 0:
            appName = str (sys.argv[0])
        print ("error parsing command line: " + message)
        print ("run \'" + appName + " --help\' for more informations.")
        os._exit (1)


    def parse(self, arguments = None):
        """
        Parse command line arguments.
        """
        # Get arguments
        if arguments != None:
            args = copy.copy (arguments)
        else:
            args = copy.copy (sys.argv)
            args.pop (0)

        # parse flags and parameters and extra arguments
        newArgs = []
        argIndex = 0
        while argIndex < len (args):
            if args[argIndex] == "--":
                # check for extra arguemnts entries
                extraEntry = None
                for p in self.entries:
                    if isinstance (p, ExtraArguments):
                        extraEntry = p
                        break
                if extraEntry == None:
                    self.commandlineInvalid ("missing option name after --")            
                else:
                    argIndex = argIndex + 1
                    additionalArgs = []
                    while argIndex < len (args):
                        additionalArgs.append (args[argIndex])
                        argIndex = argIndex + 1 
                    extraEntry.onParse (self, additionalArgs)
                    break

            elif args[argIndex].startswith ("--"):
                # check for long option entry
                argName = args[argIndex][2 : len (args[argIndex])]
                argIndex = argIndex + 1
                argFound = False
                for p in self.entries:
                    if isinstance(p, (Flag, Parameter)):
                        if p.name == argName:
                            argFound = True
                            if isinstance (p, Parameter):
                                if argIndex >= len (args):
                                    self.commandlineInvalid ("missing value after --" + argName)            
                                argValue = args[argIndex]
                                argIndex = argIndex + 1
                                pe = p.onParse (self, argValue)
                                if pe != None:
                                    self.commandlineInvalid ("parameter --" + argName + " " + pe)
                            else:
                                pe = p.onParse (self, True)
                                if pe != None:
                                    self.commandlineInvalid ("parameter --" + argName + " " + pe)
                            break
                if argFound == False:
                    self.commandlineInvalid ("option --" + argName + " is unknown")

            elif args[argIndex].startswith ("-"):
                # check for short option entry
                tok = args[argIndex][1 : len (args[argIndex])]
                if len (tok) < 1:
                    self.commandlineInvalid ("expected option after -")
                while len (tok) > 0:
                    opt = tok[0]
                    argFound = False
                    for p in self.entries:
                        if isinstance(p, (Flag, Parameter)):
                            if p.short == opt:
                                argFound = True
                                if isinstance (p, Parameter):
                                    if len (tok) > 1:
                                        argValue = tok[1 : len (tok)]
                                        tok = ""
                                    else:
                                        argIndex = argIndex + 1
                                        if argIndex >= len (args):
                                            self.commandlineInvalid ("missing value after -" + opt)
                                        argValue = args[argIndex]
                                    pe = p.onParse (self, argValue)
                                    if pe != None:
                                        self.commandlineInvalid ("parameter -" + opt + " " + pe)
                                else:
                                    pe = p.onParse (self, True)
                                    if pe != None:
                                        self.commandlineInvalid ("parameter -" + opt + " " + pe)
                                break
                    if argFound == False:
                        self.commandlineInvalid ("option -" + opt + " is unknown")
                    if len (tok) > 0:
                        tok = tok[1 : len (tok)]
                argIndex = argIndex + 1

            else:
                # pass to argument parsing
                newArgs.append (args[argIndex])
                argIndex = argIndex + 1
        args = newArgs

        # parse arguments
        for entry in self.entries:
            if isinstance (entry, Argument):
                if len (args) < 1:
                    break
                if entry.isArray:
                    pe = entry.onParse (self, args)
                    if pe != None:
                        self.commandlineInvalid ("argument " + entry.name + ": " + pe)
                    args = []
                    break
                else:
                    pe = entry.onParse (self, args[0])
                    if pe != None:
                        self.commandlineInvalid ("argument " + entry.name + ": " + pe)
                    args.pop (0)


        # assert no arguments left
        if len (args) > 0:
            self.commandlineInvalid ("invalid extra arguments: \'" + str (args[0]) + "\'")

        # assert all parameters are parsed
        for entry in self.entries:
            if isinstance (entry, Argument):
                if (entry.parsed == False) and (entry.optionalParsing == False) and (entry.isOptional == False):
                    self.commandlineInvalid ("missing argument " + str (entry.name))
    

    def dumpParsed(self, withDefaults = False, prefix = "  "):
        """
        Dump parsed command line options.
        """
        for entry in self.entries:
            if isinstance (entry, Parameter):
                if withDefaults or entry.parsed:
                    print (prefix + "--" + entry.name + " = " + str (entry.value))
            if isinstance (entry, Flag):
                if entry.parsed:
                    print (prefix + "--" + entry.name)
        for entry in self.entries:
            if isinstance (entry, Argument):
                if entry.parsed or withDefaults:
                    print (prefix + entry.name + " = " + str (entry.value))
        for entry in self.entries:
            if isinstance (entry, ExtraArguments):
                if entry.parsed or withDefaults:
                    print (prefix + "-- " + str (entry.value))
