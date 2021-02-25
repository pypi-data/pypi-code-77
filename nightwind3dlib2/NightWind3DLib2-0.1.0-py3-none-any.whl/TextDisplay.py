from direct.gui.DirectGui import *

time = 0
content = OnscreenText(text='',
                         pos=(0,0.9,0),
                         scale=0.08,
                         wordwrap=80)

def display(text):
    global time
    time += 0.01
    content.setText(text + "                                                                          " + "time:" + str(round(time,0)))
