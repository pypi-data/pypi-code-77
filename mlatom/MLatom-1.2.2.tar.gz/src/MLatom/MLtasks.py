#!/usr/bin/python3
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

import os, sys, subprocess, time, shutil, re, copy, json
import stopper
from io import StringIO
from contextlib import redirect_stdout
from math import inf, log
import interface_MLatomF

class MLtasksCls(object):
    def __init__(self, argsMLtasks = sys.argv[1:]):

        args.parse(argsMLtasks)
        argsstr = '        '
        for arg in argsMLtasks:
            argsstr += arg + ' '
        
        # Perform requested task
        if args.deltaLearn:
            self.deltaLearn()
        elif args.selfCorrect:
            self.selfCorrect()
        else:
            self.chooseMLop(args.argsIFs)

    
    @classmethod
    def deltaLearn(cls):
        locargs = args.argsIFs
        yb = [float(line) for line in open(args.Yb, 'r')]
        if args.createMLmodel or args.estAccMLmodel:
            ydatname = '%s-%s.dat' % (fnamewoExt(args.Yt), fnamewoExt(args.Yb))
            locargs = addReplaceArg('Yfile', 'Yfile=%s' % ydatname, locargs)
            yt = [float(line) for line in open(args.Yt, 'r')]
            with open(ydatname, 'w') as fcorr:
                    for ii in range(len(yb)):
                        fcorr.writelines('%25.13f\n' % (yt[ii] - yb[ii]))
            cls.chooseMLop(locargs)
        elif args.useMLmodel:
            cls.chooseMLop(locargs)
        
        if argexist('YestFile=', locargs):
            corr = [float(line) for line in open(args.YestFile, 'r')]
            with open(args.YestT, 'w') as fyestt:
                    for ii in range(len(yb)):
                        fyestt.writelines('%25.13f\n' % (yb[ii] + corr[ii]))

    @classmethod
    def selfCorrect(cls):
        locargs = args.argsIFs
        yfilename = ''
        if args.createMLmodel or args.estAccMLmodel:
            if args.createMLmodel:
                MLtaskPos = [arg.lower() for arg in locargs].index('createmlmodel')
            else:
                MLtaskPos = [arg.lower() for arg in locargs].index('estaccmlmodel')
            locargslower = [arg.lower() for arg in locargs]
            if ('sampling=structure-based' in locargslower or
                'sampling=farthest-point'  in locargslower or
                'sampling=random'          in locargslower):
                print('\n Running sampling\n')
                sys.stdout.flush()
                interface_MLatomF.ifMLatomCls.run(['sample',
                                 'iTrainOut=itrain.dat',
                                 'iTestOut=itest.dat',
                                 'iSubtrainOut=isubtrain.dat',
                                 'iValidateOut=ivalidate.dat']
                                + locargs[:MLtaskPos] + locargs[MLtaskPos+1:])
            for arg in locargs:
                if 'yfile=' in arg.lower():
                    locargs.remove(arg)
                    yfilename = arg[len('yfile='):]
        for nlayer in range(1,args.nlayers+1):
            print('\n Starting calculations for layer %d\n' % nlayer)
            sys.stdout.flush()
            if args.createMLmodel or args.estAccMLmodel:
                if nlayer == 1:
                    ydatname = yfilename
                else:
                    ydatname = 'deltaRef-%s_layer%d.dat' % (fnamewoExt(yfilename), (nlayer - 1))
                    yrefs    = [float(line) for line in open(yfilename, 'r')]
                    ylayerm1 = [float(line) for line in open('ylayer%d.dat' % (nlayer - 1), 'r')]
                    with open(ydatname, 'w') as fydat:
                        for ii in range(len(ylayerm1)):
                            fydat.writelines('%25.13f\n' % (yrefs[ii] - ylayerm1[ii]))
                for arg in locargs:
                    if ('sampling=structure-based' == arg.lower() or
                        'sampling=farthest-point'  == arg.lower() or
                        'sampling=random'          == arg.lower()):
                        locargs.remove(arg)
                        locargs += ['sampling=user-defined',
                                    'iTrainIn=itrain.dat',
                                    'iTestIn=itest.dat',
                                    'iSubtrainIn=isubtrain.dat',
                                    'iValidateIn=ivalidate.dat']
                if args.createMLmodel:
                    locargs += ['MLmodelOut=mlmodlayer%d.unf' % nlayer]
                locargs = addReplaceArg('Yfile', 'Yfile=%s' % ydatname, locargs)
                cls.chooseMLop(['YestFile=yest%d.dat' % nlayer] + locargs)
            elif args.useMLmodel:
                if nlayer > 1:
                    ylayerm1 = [float(line) for line in open('ylayer%d.dat' % (nlayer - 1), 'r')]
                cls.chooseMLop(['MLmodelIn=mlmodlayer%d.unf' % nlayer, 'YestFile=yest%d.dat' % nlayer] + locargs)
            
            if nlayer == 1:
                shutil.move('yest1.dat', 'ylayer1.dat')
            else:
                yestlayer = [float(line) for line in open('yest%d.dat' % nlayer, 'r')]
                with open('ylayer%d.dat' % nlayer, 'w') as fylayer:
                    for ii in range(len(yestlayer)):
                        fylayer.writelines('%25.13f\n' % (ylayerm1[ii] + yestlayer[ii]))
        

    @classmethod
    def chooseMLop(cls, locargs):
        interface_MLatomF.ifMLatomCls.run(locargs)
 
def fnamewoExt(fullfname):
    fname = os.path.basename(fullfname)
    fname = os.path.splitext(fname)[0]
    return fname

def argexist(argname, largs):
    for iarg in range(len(largs)):
        arg = largs[iarg]
        if argname.lower() in arg.lower():
            return True
    else:
        return False

def addReplaceArg(argname, newarg, originalargs):
    finalargs = copy.deepcopy(originalargs)
    for iarg in range(len(finalargs)):
        arg = finalargs[iarg]
        if argname.lower() == arg.split('=')[0].lower():
            finalargs[iarg] = newarg
            break
    else:
        finalargs.append(newarg)
    return finalargs

class args(object):
    # Default values:
    MLmodelType      = 'MLatomF'
    useMLmodel       = False
    createMLmodel    = False
    estAccMLmodel    = False
    # Delta-learning options
    deltaLearn       = False
    Yb               = None
    Yt               = None
    YestT            = None
    YestFile         = None
    # Self-correction options
    selfCorrect      = False
    nlayers          = 4
    
    # Only this Python program options
    argspy           = ['MLmodelType'.lower(),
                        'deltaLearn'.lower(),
                        'Yb'.lower(),
                        'Yt'.lower(),
                        'YestT'.lower(),
                        'selfCorrect'.lower()]
    # Only options of other programs
    argsIFs      = []
    
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
            
        cls.argsIFs = copy.deepcopy(argsraw)
        sys.stdout.flush()
        for arg in argsraw:
            if  (arg.lower() == 'help'
              or arg.lower() == '-help'
              or arg.lower() == '-h'
              or arg.lower() == '--help'):
                printHelp()
                stopper.stopMLatom('')
            elif arg.lower()                     == 'useMLmodel'.lower():
                cls.useMLmodel                    = True
            elif arg.lower()                     == 'createMLmodel'.lower():
                cls.createMLmodel                 = True
            elif arg.lower()                     == 'estAccMLmodel'.lower():
                cls.estAccMLmodel                 = True
            elif arg.lower()                     == 'deltaLearn'.lower():
                cls.deltaLearn                    = True


            elif arg.lower()[0:len('MLmodelType=')] == 'MLmodelType='.lower():
                cls.MLmodelType                   = arg[len('MLmodelType='):]
            elif arg.lower()[0:len('Yb=')]       == 'Yb='.lower():
                cls.Yb                            = arg[len('Yb='):]
            elif arg.lower()[0:len('Yt=')]       == 'Yt='.lower():
                cls.Yt                            = arg[len('Yt='):]
            elif arg.lower()[0:len('YestT=')]    == 'YestT='.lower():
                cls.YestT                         = arg[len('YestT='):]
            elif arg.lower()[0:len('YestFile=')] == 'YestFile='.lower():
                cls.YestFile                      = arg[len('YestFile='):]

            elif arg.lower()[0:len('XYZfile=')] == 'XYZfile='.lower():
                cls.XYZfile                      = arg[len('XYZfile='):]
            elif arg.lower()[0:len('Yfile=')] == 'Yfile='.lower():
                cls.Yfile                      = arg[len('Yfile='):]
            elif arg.lower()[0:len('YgradXYZ=')] == 'YgradXYZ='.lower():
                cls.YgradXYZ                      = arg[len('YgradXYZ='):]
            elif arg.lower()[0:len('YgradXYZestFile=')] == 'YgradXYZestFile='.lower():
                cls.YgradXYZestFile                      = arg[len('YgradXYZestFile='):] 
            elif arg.lower()[0:len('iTrainIn=')]    == 'iTrainIn='.lower():
                cls.iTrainIn                         = arg[len('iTrainIn='):]
            elif arg.lower()[0:len('iTestIn=')] == 'iTestIn='.lower():
                cls.iTestIn                      = arg[len('iTestIn='):]
            elif arg.lower()[0:len('iSubtrainIn=')]    == 'iSubtrainIn='.lower():
                cls.iSubtrainIn                         = arg[len('iSubtrainIn='):]
            elif arg.lower()[0:len('iValidateIn=')] == 'iValidateIn='.lower():
                cls.iValidateIn                      = arg[len('iValidateIn='):]
            # @Fuchun: fractional Ntrain etc?
            elif arg.lower()[0:len('Ntrain=')]    == 'Ntrain='.lower():
                cls.Ntrain                         = arg[len('Ntrain='):]
            elif arg.lower()[0:len('Nsubtrain=')]    == 'Nsubtrain='.lower():
                cls.Nsubtrain                         = arg[len('Nsubtrain='):]
            elif arg.lower()[0:len('Nvalidate=')]    == 'Nvalidate='.lower():
                cls.Nvalidate                         = arg[len('Nvalidate='):]
            elif arg.lower()[0:len('Ntest=')]    == 'Ntest='.lower():
                cls.Ntest                         = arg[len('Ntest='):]
            elif arg.lower()[0:len('sampling=')]    == 'sampling='.lower():
                cls.sampling                         = arg[len('sampling='):]
            elif arg.lower()[0:len('mlmodelout=')]    == 'mlmodelout='.lower():
                cls.mlmodelout                         = arg[len('mlmodelout='):]
            elif arg.lower()[0:len('mlmodelin=')]    == 'mlmodelin='.lower():
                cls.mlmodelin                         = arg[len('mlmodelin='):]

            elif arg.lower()                     == 'selfCorrect'.lower():
                cls.selfCorrect                   = True

            for argpy in cls.argspy:
                flagmatch = re.search(argpy, arg.lower(), flags=re.UNICODE | re.MULTILINE | re.DOTALL | re.IGNORECASE)
                if flagmatch:
                    cls.argsIFs.remove(arg)
                    break
        cls.checkArgs()
            
    @classmethod
    def checkArgs(cls):
        Ntasks = (cls.useMLmodel
                + cls.createMLmodel
                + cls.estAccMLmodel)
        if Ntasks == 0:
            printHelp()
            stopper.stopMLatom('At least one task should be requested')
        if cls.selfCorrect and (argexist('iTrainOut=', cls.argsIFs) or argexist('iTestOut=', cls.argsIFs) or argexist('iSubtrainOut=', cls.argsIFs) or argexist('iValidateOut=', cls.argsIFs)):
            printHelp()
            stopper.stopMLatom('Indices of subsets cannot be saved for self-correction')
            
def printHelp():
    if __name__ == '__main__':
        print('''
  !---------------------------------------------------------------------------! 
  !                                                                           ! 
  !              MLtasks: Scripts for ML models                               ! 
  !                                                                           ! 
  !---------------------------------------------------------------------------!
  
  Usage:
    MLtasks.py [options]
    
  Options:
      help            print this help and exit
    
    Tasks for MLtasks.py. At least one task should be requested.
    ''')
    helpText = '''
      ML operations
      useMLmodel      use existing ML model    [see interface help]
      createMLmodel   create and save ML model [see interface help]
      estAccMLmodel   estimate accuracy of ML  [see interface help]
        MLmodelType=S ML model of requested type, defines interface
                      MLatomF [default], any model available in interface to MLatomF
                      DeepMD-SE              model available in interface to DeepMD-kit
        deltaLearn    use delta-learning. Sub-options:
          Yb=S        file name with the data obtained with the baseline method
                      Sub-option for training delta-ML model
          Yt=S        file name with the reference data obtained with the target method
                      Sub-options for using delta-ML models
          YestT=S     file name with the delta-ML predictions estimating the target method
          YestFile=S  file name with the ML corrections to the baseline method
        selfCorrect   use self-correcting ML (currently works only with four layers and MLatomF)  
    '''
    print(helpText)
    sys.stdout.flush()
    print(' MLatomF help')
    sys.stdout.flush()
    interface_MLatomF.ifMLatomCls.run(['help'])
    sys.stdout.flush()
    # print(' Interface_DeePMDkit help')
    # interface_DeePMDkit.printHelp()
    # print(' Interface_GAP help')
    # interface_GAP.printHelp()

if __name__ == '__main__': 
    print(__doc__)
    MLtasks()
