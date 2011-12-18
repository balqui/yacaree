"""

Project: yacaree
Programmer: JLB

Description:

Interface 'static'-like class for provisional running of the
 tool, vt100-style
To encapsulate all "print" statements so that migration
 to Python 3 is easier
And to become a GUI some day

openfile: checks readability

Usage:
say: outputs a string message, no line breaks,
 may add a verb level clearance to allow blocking it,
 default is only say it at verb level 3
report: likewise, prepends a line break,
 variants for warnings and errors
ask_input:
 user communication

ToDo:
CLEAN UP
reorganize "choose data file"

verb: verbosity level
 0:almost silent
 1:progress rep
 2:further info
 3:a lot
progress reporting
 pongs: a dot is written every that many pong calls
 pong ("dual to ping"): acts as progress bar advance
 repong: initializes it and admits a "speed" adjustment

"""

from sys import stdout
from datetime import datetime

import statics

class iface:

    verb = 3 # ToDo: distinguish verbosity levels
##    pongs = 250 # ToDo: handle some sort of progress reporting
##    countpongs = 0
    
## ToDo: optionally several messages in the same line

##    pendinglinebreak = False

##    @classmethod
##    def say(cls,m,vb=3):
##        if cls.verb >= vb:
##            print m,
##            if statics.logfile: statics.logfile.write(m)
##            cls.pendinglinebreak = True

# report methods exported to GUI should give opportunities of interaction



    @classmethod
    def go(a,b):
        pass

    @classmethod
    def report(cls,m="",vb=3):
        print "[yacaree]", m
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @classmethod
    def possibly_report(cls,m="",vb=3):
        cls.report(m,vb)

## ToDo: handle verbosity, handle line breaks
##        "flush previous messages, write a starting message"
##        if cls.verb >= vb:
##            if cls.pendinglinebreak: 
##                print
##                if statics.logfile: statics.logfile.write("\n")
##            cls.pendinglinebreak = True

    @classmethod
    def endreport(cls):
        "flush - may become again necessary for line breaks"
        pass
    
##        if cls.pendinglinebreak: 
##            print
##            if statics.logfile: statics.logfile.write("\n")
##        cls.pendinglinebreak = False

    @classmethod
    def reportwarning(cls,m="",vb=1):
        print "[yacaree warning]", m
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

##        "flush, write warning message at low verbosity"
##        if cls.verb >= vb:
##            print

    @classmethod
    def reporterror(cls,m="",vb=0):
        print "[yacaree error] " + m
        m = "Error: " + m
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        exit(m)

##        "flush, write verbosity-independent error message, exit"
##        if cls.pendinglinebreak: 
##            print
##            if statics.logfile: statics.logfile.write("\n")

    @classmethod
    def ask_input(cls,prompt):
        if statics.logfile: statics.logfile.write("Asked:" + prompt + "\n")
        ans = raw_input(prompt)
        if statics.logfile: statics.logfile.write("Answer:" + ans + "\n")
        return ans

    @classmethod
    def openfile(cls,filename,mode="r"):
        if mode == "r":
            cls.report("Opening file " +
                       filename + " for reading.")
            try:
                f = open(filename)
                f.readline()
                f.close
                cls.report("File is now open.")
                return open(filename)
            except (IOError, OSError):
                cls.reporterror("Nonexistent or unreadable file.")
        elif mode == "w":
            cls.report("Opening file " +
                       filename + " for writing.")
            try:
                f = open(filename,"w")
                cls.report("File is now open.")
                return f
            except (IOError, OSError):
                cls.reporterror("Unable to open file.")
        else:
            cls.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")

## Progress reporting methods to be refactored

##    @classmethod
##    def repong(cls,pn=0):
##        cls.countpongs = 0
##        if pn > 0:
##            cls.pongs = pn

##    @classmethod
##    def pong(cls):
##        "not too successful attempt at progress reporting"
##        cls.countpongs += 1
##        if cls.countpongs == cls.pongs:
##            cls.say(".",1)
##            cls.countpongs = 0
