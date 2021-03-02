# Copyright (c) 2012-2020 Jicamarca Radio Observatory
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
"""Ring Buffer operation to watch a directory

"""

import os

import watchdog

from schainpy.model.proc.jroproc_base import Operation, MPDecorator

@MPDecorator
class SchainRingBuffer(Operation):

    def __init__(self):
        '''
        '''
        pass

    def run(self, dataOut, path, size=None, count=None, duration=None, interval=60):
        '''
        '''
        pass