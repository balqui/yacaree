"""
Project: yacaree
Programmer: JLB

Evolution of earlier module encompassing some static objects accessed from everywhere
(or: Singleton pattern implemented as module; spoiler: did not work well enough).

CAVEAT: IS BEING FULLY REFACTORED

iface: the actual interface, which can be textual CLI or GUI - MOVED TO yacaree.py FOR THE TIME BEING

verbose: echo all log entries to terminal - UNCLEAR

filenamext: extension assumed for dataset files if absent - UNCLEAR

logfile: potential logging file - UNCLEAR

scale: for writing ints as floats with controlled precision loss - UNCLEAR

epsilon: to compare floats to zero, try to avoid using it - TO BE REMOVED

pend_len_limit: limit on the size of the heap of closures pending for expansion - TO BE POSSIBLY REMOVED

pend_total_limit: max total length of info related to the pending closures - TO BE POSSIBLY REMOVED

boostab: stability of boost, weight of current value in front of lift values coming in - TO STAY

confthr: was about 2/3 for long, scaled; set at 0.6 for somedays, not convincing, settling for 0.65 for v1.1
(natural alternatives to consider: 3/4 and 4/5) - TO STAY

supp_rep_often: how often to report about the ongoing support - CONCEPT CHANGED, CLARIFY

findrules: process bound, don't mine more than that many rules; if zero or negative, don't apply any bound - TO BE POSSIBLY REMOVED

maxrules: number of rules to be output, max boost among those found - TO STAY BUT CLARIFY

initialboost: initial bound on the confidence boost - TO STAY

absoluteboost: NO WAY any rule reported has lower boost than that, EVER - TO STAY

genabsupp: Do not consider closures with absolute support below this - TO STAY

"""

class HyperParam:

    def __init__(self):
        
        # version = "version 1.2.2"
        # ~ version = "1.2.5"
        self.version = "2.0.0"           # MOVE THIS SOMEWHERE ELSE

        self.iface = None
        self.filenamext = ".txt"
        self.logfile = None
        self.filename = None 
        self.filenamefull = None

        self.verbose = False

        self.running = False

        self.please_report = False # To report every now and then 
        self.scale = 100000
        self.epsilon = 100.0/self.scale
        self.boostab = 5
        self.supp_rep_often = 100 # every that many closures unless verbose
        # report current support at most that many times # changed concept
        
        ## standard process:
        
        self.pend_len_limit = 16384 # 1000 # 16384 # 2 to power 14
        self.pend_total_limit = 100000000 # 100000 # 100000000
        self.pend_mem_limit = 1000000000 # 1GB
        ##confthr = int((2.0/3) * scale)
        self.confthr = int(0.65 * self.scale)
        self.findrules = 0
        self.maxrules = 50 # set this to zero if all the rules are to be written out
        self.stdmaxrules = self.maxrules # to recover the standard situation if necessary
        self.initialboost = 1.15
        self.absoluteboost = 1.05
        self.genabsupp = 5 # absolute number of transactions
        self.boostdecr = 0.001 # minimal boost decrease allowed
        self.report_period = 30 # try to show program is alive every that many seconds

    # ~ @staticmethod
    def storefilename(self, filename):
        if len(filename)<=3 or filename[-4] != '.':
            self.filename = filename
            self.filenamefull = filename + self.filenamext
        else:
            self.filename, _ = filename.rsplit('.',1)
            self.filenamefull = filename
