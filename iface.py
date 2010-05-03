"""

Project: yacaree
Programmer: JLB

Description: vt100-style interface, to be replaced by a reasonable GUI some day

verb: verbosity level (0:almost silent, 1:progress rep, 2:further info, 3:a lot)
pongs: a dot is written every that many pong calls

Usage:
say: outputs a string message, no line breaks, may add a verb level clearance
     to allow blocking it, default is only say it at verb level 3
report: likewise, prepends a line break
pong ("dual to ping"): acts as progress bar advance
repong: initializes it and admits a "speed" adjustment

"""

verb = 1

pongs = 250

countpongs = 0

def repong(pn=0):
    countpongs = 0
    if pn > 0:
        pongs = pn

def pong():
    countpongs += 1
    if countpongs == pongs:
        say(".",1)
        countpongs = 0

def say(m,vb=3):
    if verb >= vb:
        print m,

def report(m="",vb=3):
    "flush previous messages and write a starting message"
    if verb >= vb:
        print
        print m,
