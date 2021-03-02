from Fractal import *

def demo():
    fr = Fractal('F-F+F+FFF-F-F+F+F-F+F+FFF-F-F+F+F-F+F+FFF-F-F+F+F-F+F+FFF-F-F+F', 90, 4)
    fr.start()

def demo_ruled():
    code = "FX+FX+FX"
    rule = {"X": "X+YF+", "Y": "-FX-Y"}
    iterations = 7
    angle = 90
    fr = RuledFractal(code, angle, iterations, rule)
    fr.start()

demo_ruled()