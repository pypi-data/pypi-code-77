#!/usr/bin/python
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

import sys, os, subprocess, re
import stopper
mlatomdir=os.path.dirname(__file__)
mlatomfbin="%s/MLatomF" % mlatomdir

class ifMLatomCls(object):           
    @classmethod
    def run(cls, argsMLatomF, shutup=False):
        for arg in argsMLatomF:
            flagmatch = re.search('nthreads', arg.lower(), flags=re.UNICODE | re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if flagmatch:
                argsMLatomF.remove(arg)
        proc = subprocess.Popen([mlatomfbin] + argsMLatomF, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(proc.stdout.readline, b''):
          if not shutup: print(line.decode('ascii').replace('\n',''))
        proc.stdout.close()

if __name__ == '__main__':
    print(__doc__)
    ifMLatomCls.run(sys.argv[1:])
