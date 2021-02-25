#!/usr/bin/env python3
'''

  !---------------------------------------------------------------------------!
  !                                                                           !
  !     MLatom: a Package for Atomistic Simulations with Machine Learning     !
  !                          Development version                              !
  !                           http://mlatom.com/                              !
  !                                                                           !
  !                  Copyright (c) 2013-2020 Pavlo O. Dral                    !
  !                           http://dr-dral.com/                             !
  !                                                                           !
  ! All rights reserved. No part of MLatom may be used, published or          !
  ! redistributed without written permission by Pavlo Dral.                   !
  !                                                                           !
  ! The above copyright notice and this permission notice shall be included   !
  ! in all copies or substantial portions of the Software.                    !
  !                                                                           !
  ! The software is provided "as is", without warranty of any kind, express   !
  ! or implied, including but not limited to the warranties of                !
  ! merchantability, fitness for a particular purpose and noninfringement. In !
  ! no event shall the authors or copyright holders be liable for any claim,  !
  ! damages or other liability, whether in an action of contract, tort or     !
  ! otherwise, arising from, out of or in connection with the software or the !
  ! use or other dealings in the software.                                    !
  !                                                                           !
  ! Cite as: Pavlo O. Dral, J. Comput. Chem. 2019, 40, 2339-2347              !
  !                                                                           !
  !          Pavlo O. Dral, Bao-Xin Xue, Fuchun Ge, Yi-Fan Hou,               !
  !     MLatom: A Package for Atomistic Simulations with Machine Learning     !
  !                               version 1.2                                 !
  !               Xiamen University, Xiamen, China, 2013-2020.                !
  !                                                                           !  
  !---------------------------------------------------------------------------!

'''

import os, sys, subprocess, time, shutil, re, copy
import MLtasks, sliceData, stopper
import interface_MLatomF
import header
ML_NEA = __import__('ML-NEA')

class MLatomMainCls(object):
    def __init__(self):
        starttime = time.time()
        
        # print(__doc__)
        header.printHeader()
        
        print(' %s ' % ('='*78))
        print(time.strftime(" MLatom started on %d.%m.%Y at %H:%M:%S", time.localtime()))
        print('        with the following options:')
        argsstr = '        '
        for arg in sys.argv:
            argsstr += arg + ' '
        print(argsstr.rstrip())
        args.parse(sys.argv[1:])
        print(' %s ' % ('='*78))
        sys.stdout.flush()

        # Set the number of threads
        if args.nthreads:
            os.environ["OMP_NUM_THREADS"] = args.nthreads
            os.environ["MKL_NUM_THREADS"] = args.nthreads
            os.environ["OMP_PROC_BIND"]   = 'true'
        
        # Perform requested task
        if args.XYZ2X or args.sample or args.analyze:
            interface_MLatomF.ifMLatomCls.run(args.args2pass)
        elif args.slicedata or args.sampleFromSlices or args.mergeSlices:
            sliceData.sliceDataCls(argsSD = args.args2pass)
        elif args.useMLmodel or args.createMLmodel or args.estAccMLmodel or args.learningCurve:
            MLtasks.MLtasksCls(argsMLtasks = args.args2pass)
        elif args.MLNEA:
            ML_NEA.parse_api(args.args2pass)
        
        endtime = time.time()
        wallclock = endtime - starttime
        print(' %s ' % ('='*78))
        print(' Wall-clock time: %.2f s (%.2f min, %.2f hours)\n' % (wallclock, wallclock / 60.0, wallclock / 3600.0))
        print(time.strftime(" MLatom terminated on %d.%m.%Y at %H:%M:%S", time.localtime()))
        print(' %s ' % ('='*78))
        sys.stdout.flush()

class args(object):
    # Default values:
    nthreads         = None
    XYZ2X            = False
    analyze           = False
    sample           = False
    slicedata        = False
    sampleFromSlices = False
    mergeSlices      = False
    MLmodelType      = 'MLatomF'
    useMLmodel       = False
    createMLmodel    = False
    estAccMLmodel    = False
    learningCurve    = False
    # Interfaces
    callNXinterface  = False
    callDeePMD       = False
    MLNEA            = False
    AIQM2            = False

    # Only main Python program options
    argspy           = ['callNXinterface'.lower()]
    # Only options of other programs
    args2pass = []
    
    @classmethod
    def parse(cls, argsraw):
        if len(argsraw) == 0:
            printHelp()
            stopper.stopMLatom('At least one option should be provided')
        argslower = [arg.lower() for arg in argsraw]
        if ('help' in argslower
        or '-help' in argslower
        or '-h' in argslower
        or '--help' in argslower):
            printHelp()
            stopper.stopMLatom('')

        argsrawFromInputFile = []
        if len(argsraw) == 1:
            try:
                print('  Options read from input file %s' % argsraw[0])
                with open(argsraw[0], 'r') as ff:
                    for line in ff:
                        print('%s' % line.rstrip())
                        xx = line.split('#')[0]
                        if not xx == '':
                            argsrawFromInputFile += xx.split()
            except:
                printHelp()
                stopper.stopMLatom('Input file %s not found' % argsraw[0])
            argsraw = argsrawFromInputFile
            argslower = [arg.lower() for arg in argsraw]
            
        cls.args2pass = copy.deepcopy(argsraw)
        sys.stdout.flush()
        for arg in argsraw:
            if  (arg.lower() == 'help'
              or arg.lower() == '-help'
              or arg.lower() == '-h'
              or arg.lower() == '--help'):
                printHelp()
                stopper.stopMLatom('')
            elif arg.lower()[0:len('nthreads=')] == 'nthreads=':
                cls.nthreads                      = arg[len('nthreads='):].lower()

            elif arg.lower()                     == 'XYZ2X'.lower():
                cls.XYZ2X                         = True
            elif arg.lower()                     == 'analyze'.lower():
                cls.analyze                        = True
            elif arg.lower()                     == 'sample'.lower():
                cls.sample                        = True
            elif arg.lower()                     == 'useMLmodel'.lower():
                cls.useMLmodel                    = True
            elif arg.lower()                     == 'createMLmodel'.lower():
                cls.createMLmodel                 = True
            elif arg.lower()                     == 'estAccMLmodel'.lower():
                cls.estAccMLmodel                 = True
            elif arg.lower()                     == 'learningCurve'.lower():
                cls.learningCurve                 = True
                
            elif arg.lower()                     == 'selfCorrect'.lower():
                cls.selfCorrect                   = True
    
            elif arg.lower()                     == 'slice'.lower():
                cls.slicedata                     = True
            elif arg.lower()                     == 'sampleFromSlices'.lower():
                cls.sampleFromSlices              = True
            elif arg.lower()                     == 'mergeSlices'.lower():
                cls.mergeSlices                   = True
    
            elif arg.lower()                     == 'callNXinterface'.lower():
                cls.callNXinterface               = True
            elif arg.lower()                     == 'cross-section'.lower():
                cls.MLNEA                         = True
            elif arg.lower()                     == 'AIQM2'.lower():
                cls.AIQM2                         = True

            #else: # Other options are usually passed over to the interfaced programs
            #    printHelp()
            #    stopper.stopMLatom('Option "%s" is not recognized' % arg)
            for argpy in cls.argspy:
                flagmatch = re.search(argpy, arg.lower(), flags=re.UNICODE | re.MULTILINE | re.DOTALL | re.IGNORECASE)
                if flagmatch:
                    cls.args2pass.remove(arg)
                    break
            
        cls.checkArgs()
            
    @classmethod
    def checkArgs(cls):
        Ntasks = (cls.XYZ2X
                + cls.analyze
                + cls.sample
                + cls.slicedata
                + cls.sampleFromSlices
                + cls.mergeSlices
                + cls.useMLmodel
                + cls.createMLmodel
                + cls.estAccMLmodel
                + cls.learningCurve
                + cls.MLNEA)
        if Ntasks == 0:
            printHelp()
            stopper.stopMLatom('At least one task should be requested')
            
def printHelp():
    helpText = '''
  Usage:
    MLatom.py [options]
    
  Options:
      help            print this help and exit

      nthreads=N      define number of threads (N) for parallel calculations
                      By default the maximum possible number of threads is used

    Tasks for MLatom (for their suboptions see below). At least one task should be requested
      XYZ2X           convert XYZ coordinates into molecular descriptor X
      analyze         analyze data sets
      sample          sample data points from a data set
'''
    print(helpText)
    sliceData.printHelp()
    MLtasks.printHelp()
    ML_NEA.print_help()

if __name__ == '__main__':
    MLatomMainCls()
