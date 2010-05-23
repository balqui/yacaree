"""

Project: yacaree
Programmer: JLB

Description:

Interface 'static'-like class for provisional running of the
 tool, vt100-style - lowercase initial due to static use
To encapsulate all "print" statements so that migration
 to Python 3 is easier
And to become a GUI some day

verb: verbosity level - I THINK IT DOES NOT WORK YET
 0:almost silent
 1:progress rep
 2:further info
 3:a lot
pongs: a dot is written every that many pong calls
openfile: checks readability

Usage:
say: outputs a string message, no line breaks,
 may add a verb level clearance to allow blocking it,
 default is only say it at verb level 3
report: likewise, prepends a line break,
 variants for warnings and errors
pong ("dual to ping"): acts as progress bar advance
repong: initializes it and admits a "speed" adjustment

"""

import sys

class iface:

    verb = 3
    pongs = 250
    countpongs = 0
    pendinglinebreak = False

    @classmethod
    def repong(cls,pn=0):
        cls.countpongs = 0
        if pn > 0:
            cls.pongs = pn

    @classmethod
    def pong(cls):
        cls.countpongs += 1
        if cls.countpongs == cls.pongs:
            cls.say(".",1)
            cls.countpongs = 0

    @classmethod
    def say(cls,m,vb=3):
        if cls.verb >= vb:
            print m,
            cls.pendinglinebreak = True

    @classmethod
    def report(cls,m="",vb=3):
        "flush previous messages, write a starting message"
        if cls.verb >= vb:
            if cls.pendinglinebreak: 
                print
            print "[yacaree]", m,
            cls.pendinglinebreak = True

    @classmethod
    def endreport(cls):
        "flush"
        if cls.pendinglinebreak: 
            print
        cls.pendinglinebreak = False

    @classmethod
    def reportwarning(cls,m="",vb=1):
        "flush, write warning message at low verbosity"
        if cls.verb >= vb:
            print
            print "[yacaree warning]", m

    @classmethod
    def reporterror(cls,m="",vb=0):
        "flush, write verbosity-independent error message, exit"
        m = "[yacaree error] "+m
        if cls.pendinglinebreak: 
            print
        print m
        sys.exit(m)

    @classmethod
    def openfile(cls,filename):
        cls.report("Attempting to read dataset from file "+filename+"...")
        try:
            f = open(filename)
            f.readline()
            f.close
            cls.say("file is now open.")
            return open(filename)
        except (IOError, OSError):
            cls.reporterror("Nonexistent or unreadable file.")

