from time import *
from turtle import *
import os
def pint(word):
    for i1 in word:
        print(i1,end='',flush=True)
def stamp(something,speed,FT):
    number = 0
    for i in range(len(something)):
        print(something[number],end = "")
        sleep(speed)
        number += 1
    if FT == 1:
        print()
    sleep(0.5)
'''turprint(some,size,x,y),括号里some的位置填想打印的文本，size的位置填文本大小,place的位置填"center"、"left"、"right"等'''
def turprint(some,size,place):
    pen = Turtle()
    pen.hideturtle()
    pen.penup()
    write(some,align=place,font=("微软雅黑", size,"normal"))
def clear():
    print("\033[2J""")
    pint("\033[99999A")
def clean():
    os.system("clear")
def steap(something1,speed1):
    clear()
    stamp(something1,speed1)