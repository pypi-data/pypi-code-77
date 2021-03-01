import json
import sys,os

def printHeader():

    header = '''

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
    print(header)

    with open(os.path.dirname(__file__)+'/ref.json','r') as f:
        ref = json.load(f)
    args.parse(sys.argv[1:])
    
    refItem = []
    if args.mlmodeltype.lower() == 'mlatomf':
        if args.selfcorrect:
            refItem.append("Self-Correct")
        if args.deltalearn:
            refItem.append('deltalearn')
        if args.xyz2x or args.sampling.lower() == 'structure-based' or ((args.estaccmlmodel or args.createmlmodel) and args.xyzfile):
            if args.moldescriptor.lower() == 'cm':
                refItem.append("Coulomb Matrix")
            elif args.moldescriptor.lower() == 're':
                refItem.append("RE Descriptor")
        if args.sampling.lower() == 'structure-based':
            refItem.append("Structure-based Sampling")
    if refItem:
        print('*'*80)
        print(' You are going to use feature(s) listed below. \n Please cite corresponding work(s) in your paper:')
        for i in refItem:
            if i in ref.keys():
                print('\n %s:\n\t%s'%(i,ref[i]))


    
class args(object):
    mlmodeltype = 'mlatomf'
    sampling = 'random'
    selfcorrect = False
    deltalearn = False
    moldescriptor = 're'
    xyz2x = False
    createmlmodel = False
    estaccmlmodel = False
    xyzfile = ''

    @classmethod
    def parse(cls, argsraw):
        if len(argsraw) == 1:
            try:
                argsrawFromInputFile = []
                with open(argsraw[0], 'r') as ff:
                    for line in ff:
                        print('%s' % line.rstrip())
                        xx = line.split('#')[0]
                        if not xx == '':
                            argsrawFromInputFile += xx.split()
                argsraw = argsrawFromInputFile
            except:
                pass
        for arg in argsraw:
            if len(arg.lower().split('=')) == 1:                             # parse boolean args
                try:
                    exec('cls.'+arg.lower())
                    exec('cls.'+arg.lower()+'=True')
                except: pass
            else:                                               # parse other args
                try:
                    exec('cls.'+arg.split('=')[0].lower())
                    if type(eval('cls.'+arg.split('=')[0].lower())) == str :
                        exec('cls.'+arg.split('=')[0].lower()+'='+"arg.split('=')[1]")
                    else:
                        exec('cls.'+arg.split('=')[0].lower()+'='+arg.split('=')[1])
                except:
                    pass
