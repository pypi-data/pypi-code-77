import os
import copy
import pathlib
from . import attributes
from . import algorithms
from .util import hash
from .util import cache
from .util import commandline
from .util import materializer
from .util import encoder
from .util import parallel




def parseCameraPosition(text: str):
    parts = text.split (',')
    result = []
    if len (parts) in (6, 7):
        for p in parts:
            if re.match(r'^-?\d+(?:\.\d+)?$', p) is None:
                return None
            result.append (float (p))
        return result
    else:
        return None




def ParameterFilterCamera(param, value):
    result = parseCameraPosition (value)
    if result == None:
        return "invalid camera vector"
    return None




class _ToolRunner:
    """
    Class for building command line rendering tools.
    """
    def __init__ (self,
                    appName,
                    appGenerateScene,
                    appDescription,
                    appAnimators,
                    appCmdOptions,
                    appDefaultAttributes
        ):

        #: Name of the application.
        self.appName = appName

        #: Generator function for the scene.
        self.appGenerateScene = appGenerateScene

        #: Description of the application.
        self.appDescription = appDescription

        #: Animators supplied by application.
        self.appAnimators = appAnimators

        #: Additional command line options.
        self.appCmdOptions = appCmdOptions

        #: Default attributes from application
        self.appDefaultAttributes = appDefaultAttributes if appDefaultAttributes != None else attributes.Attributes.defaults ()

        # Create command line parser
        self.parser = commandline.Parser (self.appName, self.appDescription)

        # What to do?
        actions = {
            'duration':     {'description': 'Returns the animations duration in seconds.'},
            'generate':     {'description': 'Generate a script to be used by the materializer.'},
            'render':       {'description': 'Render an image.'},
            'generateseq':  {'description': 'Generate a sequence of scripts to be used together with materializer by running animators.'},
            'renderseq':    {'description': 'Render an image sequence by running animators.'},
            'animation':    {'description': 'Create animation as video file.'},
            'parts':        {'description': 'Create a list of maufacturable parts and their count.'},
            'manufacture':  {'description': 'Create maufacturing data for all parts or a single part.'},
        }
        self.argAction = commandline.ArgumentChoose ("action", "Action to perform:", actions)

        # Output file prefix
        self.argOutput = commandline.Argument ("output", "Prefix of output file name.", False, True)

        # Create command line options: rendering options
        renderingGroup = "Rendering options"
        self.optTime = commandline.Parameter (
            "time",
            "t",
            "Time of animation begin or animation time for a single frame.",
            renderingGroup,
            "0.0",
            "t",
            commandline.FilterNumber
        )

        self.optTimeScale = commandline.Parameter (
            "timescale",
            "s",
            "Scale factor for animation time.",
            renderingGroup,
            1,
            "factor",
            commandline.FilterNumberGreterZero
        )

        self.optDuration = commandline.Parameter (
            "duration",
            "d",
            "Duration of sequence or animation.",
            renderingGroup,
            None,
            "d",
            commandline.FilterNumber
        )

        self.optWidth = commandline.Parameter (
            "width",
            "w",
            "Width of image in pixels.",
            renderingGroup,
            "1920",
            "w",
            commandline.FilterIntegerGreterZero
        )

        self.optHeight = commandline.Parameter (
            "height",
            "h",
            "Height of image in pixels.",
            renderingGroup,
            "1080",
            "h",
            commandline.FilterIntegerGreterZero
        )

        self.optFps = commandline.Parameter (
            "fps",
            "f",
            "Number of frames per second, used for sequences and animations.",
            renderingGroup,
            "60.0",
            "fps",
            commandline.FilterNumberGreterZero
        )

        self.optAntialias = commandline.Parameter (
            "antialias",
            "a",
            "Anti aliasing setting in range 1..12, higher values will look smoother.",
            renderingGroup,
            "1",
            "val",
            commandline.FilterIntegerGreterZero
        )

        self.optQuality = commandline.Parameter (
            "quality",
            "q",
            "Render quality setting in range 1..12, higher values will look better.",
            renderingGroup,
            "1",
            "val",
            commandline.FilterInteger
        )

        renderMinAngle, renderMinSize, renderFixedCount, renderMinSlices = self.appDefaultAttributes.rasterizingAttributes ()

        self.optFa = commandline.Parameter (
            "fa",
            None,
            "Maximum angle difference between segments when rasterizing shapes and solids in degrees.",
            renderingGroup,
            renderMinAngle,
            "fa",
            commandline.FilterNumberGreterZero
        )

        self.optFs = commandline.Parameter (
            "fs",
            None,
            "Maximum distance error of segment when rasterizing shapes and solids in units.",
            renderingGroup,
            renderMinSize,
            "fs",
            commandline.FilterNumberGreterZero
        )

        # collect manufacture and render formats
        maunfactureRenderFormats = {}
        for m in materializer.getMaterializers ():
            for e in m.materializeExtensions ():
                if not e in maunfactureRenderFormats:
                    maunfactureRenderFormats[e] = {}
        for m in materializer.getMaterializers ():
            for e in m.renderExtensions ():
                if not e in maunfactureRenderFormats:
                    maunfactureRenderFormats[e] = {}


        self.optManufactureRenderType = commandline.ParameterChoose (
            "fmt", 
            "M",
            "Format for manufacturing or rendering files.",
            renderingGroup,
            maunfactureRenderFormats,
            None,
            "format"
        )

        # collect encoding presets from encoder registry
        encodingPresets = {}
        for encoderInstance in encoder.getEncoders ():
            for preset in encoderInstance.presets ():
                encodingPresets[encoderInstance.name () + '.' + str (preset)] = {}

        defaultEncodingFormat = None
        if len (encoder.getEncoders ()) > 0:
            enc = encoder.getEncoders ()[0]
            defaultEncodingFormat = enc.name () + '.' + enc.defaultPreset ()

        self.optEncode = commandline.ParameterChoose (
            "encoding", 
            "e", 
            "Video encoding preset, affects quality and encoding time", 
            renderingGroup, 
            encodingPresets, 
            defaultEncodingFormat,
            "preset"
        )

        self.optCamera = commandline.Parameter (
            "camera",
            "c",
            "Override camera vector.",
            renderingGroup,
            None,
            "view",
            ParameterFilterCamera
        )

        projections = {
            'perspective':          {'description' : 'Use perspective projection.'},
            'orthogonal':           {'description' : 'Use orthogonal projection.'}
        }

        self.optProjection = commandline.ParameterChoose (
            "projection",
            "p",
            "Projection type used for rendering.",
            renderingGroup,
            projections,
            None,
            "p"
        )

        self.optPreview = commandline.Flag (
            "preview",
            "P",
            "Preview frame while rendering",
            renderingGroup
        )

        self.optPartFilter = commandline.Parameter (
            "parts",
            'S',
            "Filter string for parts to manufacture.",
            renderingGroup,
            "*",
            "filter"
        )

        # Create command line options: miscellanous options
        miscGroup = "Miscellaneous options"
        self.optHelp = commandline.Flag (
            "help",
            None,
            "Show help.",
            miscGroup,
            self._showHelp
        )

        self.optCache = commandline.Parameter (
            "cache",
            None,
            "Path of cache directory.",
            miscGroup,
            ".pcsg.cache",
            "cache"
        )

        self.optJobs = commandline.Parameter (
            "jobs",
            "j",
            "Number of jobs to execute in parallel.",
            miscGroup,
            1,
            "jobs",
            commandline.FilterIntegerGreterZero
        )

        self.optNice = commandline.Parameter (
            "nice",
            "n",
            "Nice level [0..19] for process, higher nice level has lower priority.",
            miscGroup,
            "15",
            "nice",
            commandline.FilterInteger
        )

        self.optZeroOutput = commandline.Flag (
            "zero-output",
            "z",
            "Disable output of status.",
            miscGroup
        )


        # List of materializers
        materializers = {}
        for m in materializer.getMaterializers ():
            materializers[m.name ()] = {}
        self.optMaterializer = commandline.ParameterChoose ("materializer", "m", "Select materializer", miscGroup, materializers, "openscad", "m")

        # last progress display string
        self.lastProgress = ""


    def _registerToolOptions (self):
        # arguments
        self.parser.register (self.argAction)
        self.parser.register (self.argOutput)

        # rendering group
        self.parser.register (self.optTime)
        self.parser.register (self.optTimeScale)
        self.parser.register (self.optDuration)
        self.parser.register (self.optWidth)
        self.parser.register (self.optHeight)
        self.parser.register (self.optFps)
        self.parser.register (self.optQuality)
        self.parser.register (self.optAntialias)
        self.parser.register (self.optEncode)
        self.parser.register (self.optCamera)
        self.parser.register (self.optProjection)
        self.parser.register (self.optPreview)
        self.parser.register (self.optFa)
        self.parser.register (self.optFs)
        self.parser.register (self.optManufactureRenderType)
        self.parser.register (self.optPartFilter)

        # misc group
        self.parser.register (self.optHelp)
        self.parser.register (self.optMaterializer)
        self.parser.register (self.optCache)
        self.parser.register (self.optJobs)
        self.parser.register (self.optNice)
        self.parser.register (self.optZeroOutput)


    def _showHelp (self, *skip):
        """
        Show help an exit.
        """
        self.parser.showHelp ()
        os._exit (0)


    def _getDuration(self):
        """
        Get duration of animation.
        """
        maxDuration = 0
        if self.appAnimators != None:
            for animation in self.appAnimators:
                d = animation.getAnimationTime ()
                if d > maxDuration:
                    maxDuration = d
        return maxDuration


    def _doDuration(self):
        """
        Print duration of animation.
        """
        if self.optZeroOutput.value != True:
            print (str (self._getDuration ()))


    def _createJob (self, baseAttributes, materializer, time):
        """
        Creates a basic job
        """
        job = {}
        job['baseAttributes'] = baseAttributes  # basic attributes
        job['csg'] = None                       # storage for csg tree
        job['attributes'] = None                # resolved attributes
        job['csgHash'] = None                   # hash code of csg tree including attributes and calculated animations
        job['time'] = time                      # scene time
        job['animations'] = None                # precalculated animation positions 
        job['materializer'] = materializer      # materializer instance
        job['description'] = None               # job description for batch processing
        return job


    def _calculateAnimations (self, attributes, time):
        """
        Computes the animator positions for a render job.
        """
        positions = {}
        if self.appAnimators != None:
            for animation in self.appAnimators:
                positions["animations." + animation.name] = animation.getPosition (time)
        return positions


    def _createJobGenerate (self, baseAttributes, materializer, time, scriptFile = None):
        """
        Creates a generate job
        """
        job = self._createJob (baseAttributes, materializer, time)
        job['scriptCacheFile'] = None               # absolute path of generated cache file
        job['scriptFile'] = scriptFile              # target file name without extension, when output file should be copied
        job['description'] = "Generating " + materializer.name () + " script"
        job['runner'] = self._runJobGenerate        # runner function for job
        return job


    def _createJobRender (self, baseAttributes, materializer, time, extension, imageFile = None):
        """
        Creates a render job
        """
        job = self._createJob (baseAttributes, materializer, time)
        job['imageCacheFile'] = None                # absolute path of generated cache file
        job['imageFile'] = imageFile                # target file name without extension, when output file should be copied
        job['extension'] = extension                # extension for rendered file
        job['description'] = "Rendering " + extension + " image"
        job['runner'] = self._runJobRender          # runner function for job
        return job


    def _createJobEncode (self, baseAttributes, materializer, time, renderJobs, encoderInstance, encoderPreset, fps, animationFile = None):
        """
        Creates an encoding job
        """
        job = self._createJob (baseAttributes, materializer, time)
        job['renderJobs'] = renderJobs              # list of frame render jobs
        job['encoderInstance'] = encoderInstance    # encoder to use for video rendering
        job['encoderPreset'] = encoderPreset        # preset to be used for encoding
        job['fps'] = fps                            # target frames per second
        job['animationFile'] = animationFile        # target file name without extension, when output file should be copied
        job['description'] = "Encoding video"       # job description
        job['runner'] = self._runJobEncode          # runner function for job
        return job


    def _createJobManufacture (self, baseAttributes, materializer, part, partName, extension):
        """
        Creates a manufacturing job
        """
        job = self._createJob (baseAttributes, materializer, 0)
        job['part'] = part                          # part to manufacture
        job['partName'] = partName                  # file name of manufactured part
        job['description'] = "Manufacturing part"   # job description
        job['runner'] = self._runJobManufacture     # runner function for job
        job['extension'] = extension                # file extension for manufactured parts
        return job


    def _runJob (self, job):
        """
        Runnable for abstract job
        """
        # get attributes
        attrs = job['baseAttributes']

        # calculate animations
        if job['animations'] == None:
            job['animations'] = self._calculateAnimations (attrs, job['time'])

        # merge animators to attributes
        attrs = attrs.override (job['animations'])

        # merge camera settings
        cameraAttributes = attrs.cameraAttributes ()
        cameraView = cameraAttributes['view']
        cameraProjection = cameraAttributes['projection']

        # override camera attributes of scene from animations
        if 'animations.camera' in job['animations']:
            cameraView = job['animations']['animations.camera']

        # override camera settings from commandline
        attrs = attrs.override ({'camera.view': cameraView, 'camera.projection': cameraProjection})
        if self.optCamera.value != None:
            cameraView = parseCameraPosition (self.optCamera.value)
        if self.optProjection.value != None:
            cameraProjection = self.optProjection.value

        # set resolved attributes
        job['attributes'] = attrs

        # generate csg tree?
        if job['csg'] == None:
            job['csg'] = self.appGenerateScene (attrs)
            job['csgHash'] = hash (job['csg'])

        # okay, we are done.
        return True


    def _runJobGenerate (self, job):
        """
        Executes a generate job
        """
        # parent processing.
        if self._runJob (job) == False:
            return False

        # generate script and copy output file if requested
        job['scriptCacheFile'] = job['materializer'].script (job['csg'], job['attributes'], job['scriptFile'])
        return True


    def _runJobRender (self, job):
        """
        Executes a generate job
        """
        # parent processing.
        if self._runJob (job) == False:
            return False

        # generate script and copy output file if requested
        job['imageCacheFile'] = job['materializer'].render (job['csg'], job['attributes'], job['imageFile'], job['extension'])
        return True


    def _runJobEncode (self, job):
        """
        Executes an encode job
        """
        # parent processing.
        if self._runJob (job) == False:
            return False

        # collect frames and call encoder
        frames = []
        for renderJob in job['renderJobs']:
            frames.append (renderJob['imageCacheFile'])
        encoderInstance = job['encoderInstance']
        encoderPreset = job['encoderPreset']
        destPath = job['animationFile'] + '.' + encoderInstance.extension ()
        fps = job['fps']
        encoderInstance.encode (frames, fps, destPath, encoderPreset)
        return True


    def _runJobManufacture (self, job):
        """
        Runs a manufacturing job.
        """
        # parent processing.
        if self._runJob (job) == False:
            return False

        # get part details
        part = job['part']
        partName = job['partName']
        mat = job['materializer']
        attr = job['baseAttributes']
        extension = job['extension']

        # run materializer
        mat.materialize (part, attr, partName, extension)
        return True


    def _mapParts (self, baseAttributes, materializer):
        # create job to get a csg tree instance
        job = self._createJob (baseAttributes, materializer, 0)
        self._runJob (job)

        # collect parts
        parts = algorithms.CollectParts.execute (job['csg'], baseAttributes)
        collected = {}
        for part in parts:
            name = part.partName
            if name in collected:
                # check if part inside is the same
                assert part.children[0] == collected[name]['item'], "Two parts with the same name must have equal children."
                collected[name]['count'] += 1
            else:
                # just insert
                collected[name] = {'count': 1, 'item': part.children[0]}
        return collected


    @staticmethod
    def _filterMatchesPart (partName, filter):
        # check if part name is matched by filter
        if filter in ('', '*'):
            return True
        if filter[-1] == '*':
            if partName.startswith (filter[0:len(filter) - 1]):
                return True
        else:
            if partName == filter:
                return True
        return False


    def _filterPartName (self, partName):
        # query part filter from command line
        filters = self.optPartFilter.value.split (',')
        if filters == None:
            return True
        if len (filters) == 0:
            return True
        
        # check filters to match
        for f in filters:
            if _ToolRunner._filterMatchesPart (partName, f):
                return True

        # filter not matched
        return False


    @staticmethod
    def _encodePartName (partName):
        assert isinstance (partName, str)
        result = ""
        for ch in partName:
            if (ord (ch) >= ord ('a')) and (ord (ch) <= ord ('z')):
                result += ch
            elif (ord (ch) >= ord ('A')) and (ord (ch) <= ord ('Z')):
                result += ch
            elif (ord (ch) >= ord ('0')) and (ord (ch) <= ord ('9')):
                result += ch
            elif ch in ("-", "_", "."):
                result += ch
            elif ch in (" ", "\t", "\r", "\n"):
                result += "-"
            else:
                result += "_"
        return result


    def run (self, cmdArguments = None):
        """
        Run the command line tool.
        """
        # parse command line options
        self._registerToolOptions ()
        self.parser.parse (cmdArguments)

        # set nice level
        nice = 15
        nice = int (self.optNice.value)
        if nice < 0:
            nice = 0
        if nice > 19:
            nice = 19
        os.nice (nice)

        # initialize cache
        cache.setup (self.optCache.value)

        # run duration action?
        if self.argAction.value == "duration":
            self._doDuration ()
            return

        # check if materializer is valid
        mat = materializer.getMaterializer (self.optMaterializer.value)
        if mat == None:
            self.parser.commandlineInvalid ('Invalid materializer')
        matErr = mat.assertUsable ()
        if matErr != None:
            self.parser.commandlineInvalid ('Can not use materializer ' + self.optMaterializer.value + ': ' + matErr)

        # check if encoder is valid
        if self.argAction.value == 'animation':
            encoderInstance, encoderPreset = encoder.parseSettings (self.optEncode.value)
            if encoderInstance == None:
                self.parser.commandlineInvalid ("Invalid encoder settings.")
            encErr = encoderInstance.assertUsable ()
            if encErr != None:
                self.parser.commandlineInvalid ('Can not use video encoding preset ' + self.optEncode.value + ': ' + encErr)

        # setup basic attributes
        ovs = {}
        # rendering attributes
        if self.optWidth.value != None:
            ovs['render.width'] = int (self.optWidth.value)
        if self.optHeight.value != None:
            ovs['render.height'] = int (self.optHeight.value)
        if self.optQuality.value != None:
            # TODO: assert range in parser
            ovs['render.quality'] = int (self.optQuality.value)
        if self.optAntialias.value != None:
            # TODO: assert range in parser
            ovs['render.antialias'] = int (self.optAntialias.value)
        # rasterizing attributes
        if self.optFa.value != None:
            ovs['rasterize.minAngle'] = float (self.optFa.value)
        if self.optFs.value != None:
            ovs['rasterize.minSize'] = float (self.optFs.value)
        # create basic attributes
        baseAttributes = self.appDefaultAttributes.override (ovs)


        # get start time for rendering
        startTime = 0
        if self.optTime.value != None:
            startTime = float (self.optTime.value)

        # calculate duration for animations and sequences
        if self.optDuration.value != None:
            duration = float (self.optDuration.value)
        else:
            duration = self._getDuration () - startTime
            if duration < 0:
                duration = 0
        if duration < 0:
            self.parser.commandlineInvalid ("Duration must be positive.")

        # create sequence?
        if self.argAction.value in ('generateseq', 'renderseq', 'animation'):
            # create sequence
            sequence = []
            fps = float (self.optFps.value)
            if self.optTimeScale.value != None:
                timeScale = float (self.optTimeScale.value)
            else:
                timeScale = 1
            endTime = startTime + duration
            timePerFrame = 1.0 / (fps * timeScale)
            currentTime = startTime
            sequenceId = 0
            while (currentTime < endTime):
                sequence.append ((currentTime, "_%06d" % (sequenceId,)))
                currentTime += timePerFrame
                sequenceId += 1

            # render single frame if sequence is empty.
            if len (sequence) == 0:
                sequence = [(startTime, '')]
        else:
            # only generate a single frame
            sequence = [(startTime, '')]

        # run parts action?
        if self.argAction.value == "parts":
            if self.optZeroOutput.value != True:
                partMap = self._mapParts (baseAttributes, mat)
                for part in partMap:
                    partName = _ToolRunner._encodePartName (part)
                    print (str (partMap[part]['count']) + " " + partName)
            return

        # Ensure output is set
        if self.argOutput.value == None:
            self.parser.commandlineInvalid ("missing argument output")

        # initialize empty job queue
        jobQueue = []

        # run generate action?
        if self.argAction.value in ('generate', 'generateseq'):
            jobs = []
            for item in sequence:
                scriptFileName = str (pathlib.Path (self.argOutput.value + item[1]).resolve ())
                jobs.append (self._createJobGenerate (baseAttributes, mat, item[0], scriptFileName))
            jobQueue.append (jobs)

        # run render action?
        elif self.argAction.value in ('render', 'renderseq'):
            # check selected render format:
            renderFormatExtension = mat.renderDefaultExtension ()
            if self.optManufactureRenderType.value != None:
                renderFormatExtension = self.optManufactureRenderType.value
            
            # check if extension is supported
            if not renderFormatExtension in mat.renderExtensions ():
                self.parser.commandlineInvalid ("Can not use output format ." + renderFormatExtension + " to render images with " + mat.name () + ".")

            jobs = []
            for item in sequence:
                renderImageName = str (pathlib.Path (self.argOutput.value + item[1]).resolve ())
                jobs.append (self._createJobRender (baseAttributes, mat, item[0], renderFormatExtension, renderImageName))
            jobQueue.append (jobs)

        # run animation action?
        elif self.argAction.value == "animation":
            # using fixed rendering format for animations
            renderFormatExtension = 'png'

            # append rendering job for each frame
            renderJobs = []
            for item in sequence:
                renderJobs.append (self._createJobRender (baseAttributes, mat, item[0], renderFormatExtension, None))
            jobQueue.append (renderJobs)

            # animation output path without file extension
            animationOutput = str (pathlib.Path (self.argOutput.value))

            # create encoding job
            encJob = self._createJobEncode (baseAttributes, mat, startTime, renderJobs, encoderInstance, encoderPreset, fps, animationOutput)
            jobQueue.append ([encJob])

        # run manufacture action?
        elif self.argAction.value == "manufacture":
            # map parts
            partMap = self._mapParts (baseAttributes, mat)

            # get materialize format extension
            matFormatExtension = mat.materializeDefaultExtension ()
            if self.optManufactureRenderType.value != None:
                matFormatExtension = self.optManufactureRenderType.value
            
            # check if extension is supported
            if not matFormatExtension in mat.materializeExtensions ():
                self.parser.commandlineInvalid ("Can not use output format ." + matFormatExtension + " to materialize parts with " + mat.name () + ".")

            # filter parts
            partsToProcess = []
            for part in partMap:
                partName = _ToolRunner._encodePartName (part)
                if self._filterPartName (partName):
                    partsToProcess.append ((partName, partMap[part]))

            # create manufacture jobs
            manufactureJobs = []
            for part in partsToProcess:
                partFileName = str (pathlib.Path (self.argOutput.value)) + '_' + part[0]
                manufactureJobs.append (self._createJobManufacture (baseAttributes, mat, part[1]['item'], partFileName, matFormatExtension))

            # queue manufacture jobs
            jobQueue.append(manufactureJobs)

        # failed: action not handled.
        else:
            assert False, "Internal error: action not handled"

        # multi process job queues
        threadCount = int (self.optJobs.value)
        if threadCount < 1:
            threadCount = 1
        if threadCount > 64:
            threadCount = 64
        for block in jobQueue:
            pRunner = parallel.ParallelRunner (block, self._progessCallback)
            pRunner.execute (threadCount)
            self._endProgress ()

        # continue processing
        return True


    def _isConsole (self):
        # TODO: get on runtime
        # deactivate with --debug parameter 
        return True


    def _endProgress (self):
        """
        End of progress display.
        """
        if self.lastProgress != None:
            if self.optZeroOutput.value != True:
                if self._isConsole ():
                    print ("")
        self.lastProgress = None


    def _progessCallback (self, description, elementIndex = None, elementCount = None):
        """
        Diplay current progresss.
        """
        text = description
        if elementCount != None:
            if elementIndex != None:
                text = description + " (" + str (elementIndex) + " / " + str (elementCount) + ")"
        else:
            if elementIndex != None:
                text = description + " (" + str (elementIndex) + ")"
        text = "  " + text

        # TODO: implement displaying on console
        if not self._isConsole ():
            if self.optZeroOutput.value != True:
                print (text)
        else:
            llLen = len (self.lastProgress) if self.lastProgress != None else 0
            tlen = len (text)
            if tlen < llLen:
                text = text + " " * (llLen - tlen)
            if self.optZeroOutput.value != True:
                print (text + "\r", end = "")
            self.lastProgress = text




class Tool:
    """
    Base class for implementing own command line tools.
    """
    def __init__ (self,
                    name: str = None,
                    description: str = None
        ):

        #: Name of tool
        self.name = name

        #: Description of tool.
        self.description = description

        #: Command line options of tool.
        self.options = []

        #: Animators of tool.
        self.animators = []


    def addAnimation (self, animation):
        """
        Adds an animation to this tool.
        """
        self.animators.append (animation)


    def addOption (self, option):
        """
        Add a command line option to the tool.
        """
        self.options.append (option)


    def attributes (self):
        """
        Returns the default attributes to be applied on processing.
        """
        return attributes.Attributes.defaults ()


    def scene (self, attributes):
        """
        Generate a scene (csg tree).
        """
        assert False, "To be implemented by child class"


    def run (self, commandLineArgs: list = None):
        """
        Runs the tool.
        """
        t = _ToolRunner (self.name, self.scene, self.description, self.animators, self.options, self.attributes ())
        return t.run (commandLineArgs)
