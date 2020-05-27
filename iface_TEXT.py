"""

Project: yacaree
Programmer: JLB

Description:

Textual command-line interface, 
originally previous to the GUI and now concurrent with it

Planned to include some progress reporting 
(dot-based error-bar-like) and verbosity levels.
I might reconsider that in the future but, for now,
I remove everything of the sort.

Usage:
say: outputs a string message, no line breaks,
 may add a verb level clearance to allow blocking it,
 default is only say it at verb level 3
report: likewise, prepends a line break,
 variants for warnings and errors
ask_input:
 user communication
go:
 calls run method of miner, matching approximately 
 the similar button and callback of the GUI

ToDo: optionally several messages in the same line?

Opening of all files reported to log file... except opening of log file.
"""

from sys import stdout
from datetime import datetime
from six.moves import input as raw_input
import statics

class iface:

    @classmethod
    def go(cls, yacaree):
        cls.report("This is yacaree, version " + statics.version + ".")
        if statics.filenamefull is None:
            cls.reportwarning("No dataset file specified.")
            filename = cls.ask_input("Dataset File Name? ")
            cls.storefilename(filename)
        if statics.maxrules == 0:
            cls.report("Running for all rules.")
        yacaree.standard_run() # no need to call run_all as maxrules already at 0

    @classmethod
    def storefilename(cls, filename):
        if len(filename)<=3 or filename[-4] != '.':
            statics.filename = filename
            statics.filenamefull = filename + statics.filenamext
        else:
            '''statics.filenamext should not be modified:
            o/w if a new dataset is loaded, the default extension no longer applies
            '''
            # ~ statics.filename, statics.filenamext = filename.rsplit('.',1)
            statics.filename, _ = filename.rsplit('.',1)
            statics.filenamefull = filename
        # ~ cls.report("Selected dataset in file " + statics.filenamefull)

    @classmethod
    def report(cls,m=""):
        print("[yacaree] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @classmethod
    def report_log_file(cls, filename):
        "not reported like the rest for lack of log file"
        if statics.logfile: 
            "print already done, here just log entry"
            m = "Log file " + filename + ".log (this file) set up."
            statics.logfile.write(str(datetime.now()) + " " + m + "\n")
            stdout.flush()

    @classmethod
    def endreport(cls):
        "flush - may become again necessary for line breaks"
        pass
    
    @classmethod
    def reportwarning(cls,m=""):
        print("[yacaree warning] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @classmethod
    def reporterror(cls,m=""):
        # ~ print("[yacaree error] " + m)
        m = m + " Exiting.\n"
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m)
        exit("[yacaree error] " + m)

    @classmethod
    def ask_input(cls,prompt):
        "See import from six.moves above"
        if statics.logfile: statics.logfile.write("Asked:" + prompt + "\n")
        ans = raw_input(prompt)
        if statics.logfile: statics.logfile.write("Answer:" + ans + "\n")
        return ans

    @classmethod
    def openfile(cls,filename,mode="r"):
        "checks for readability"
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

    @classmethod
    def sound_bell(a):
        print('\a')

## Temporary stand-ins for GUI-related calls

    @classmethod
    def disable_filepick(a):
        pass

    @classmethod
    def disable_finish(a):
        pass

    @classmethod
    def disable_run(a):
        pass

    @classmethod
    def enable_again(a):
        pass

    @classmethod
    def enable_finish(a):
        pass
