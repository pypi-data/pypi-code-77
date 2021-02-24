import os
import signal
from typing import List, Union
import hither as hi

class KeyboardInterruptHandler(object):
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        print('SIGINT received. Preventing KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)

def start_app(*, api_websocket: bool, api_http: bool, client_dev: bool, client_prod: bool):
    thisdir = os.path.dirname(os.path.realpath(__file__))

    scripts: List[hi.ShellScript] = []

    if api_websocket:
        s = hi.ShellScript(f'''
        #!/bin/bash

        export LABBOX_EXTENSIONS_DIR={thisdir}/extensions
        export LABBOX_WEBSOCKET_PORT=10408

        exec labbox_start_api_websocket
        ''')
        scripts.append(s)
    
    if api_http:
        s = hi.ShellScript(f'''
        #!/bin/bash

        export LABBOX_HTTP_PORT=10409

        exec labbox_start_api_http
        ''')
        scripts.append(s)
    
    if client_dev:
        s = hi.ShellScript(f'''
        #!/bin/bash

        cd {thisdir}/../..
        export PORT=10407
        exec yarn start
        ''')
        scripts.append(s)
    
    if client_prod:
        s = hi.ShellScript(f'''
        #!/bin/bash

        cd {thisdir}
        exec serve -l 10407 build
        ''')
        scripts.append(s)
    
    if len(scripts) == 0:
        return

    for s in scripts:
        s.start()

    def stop_all():
        for s in scripts:
            if s.isRunning():
                s.stop()
    
    signal.signal(signal.SIGINT, stop_all)

    while True:
        all_running = True
        for s in scripts:
            if not s.isRunning():
                all_running = False
        if not all_running:
            stop_all()
            return
        for s in scripts:
            s.wait(0.1)