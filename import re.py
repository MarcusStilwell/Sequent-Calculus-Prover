#!/usr/bin/python2
import re

L_FALSE = ""
AXIOAM  = ""

NOT_LEFT  = ""
NOT_RIGHT = ""

AND_LEFT  = ""
AND_RIGHT = ""

OR_LEFT  = ""
OR_RIGHT = ""

ARROW_LEFT  = "((.*),)*((.*)->(.*?))(,(.*))*=>(.*)"
ARROW_RIGHT = "(.*)=>((.*),)*(.*)->(.*)(,(.*))*"

inp = raw_input(": ")
print re.search(ARROW_LEFT, inp)

def not_left():
    pass

def not_right():
    pass

def and_left():
    pass

def and_right():
    pass