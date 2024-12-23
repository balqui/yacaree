"""

Project: yacaree
Programmer: JLB

Module encompassing some static objects accessed from everywhere

(or: Singleton pattern implemented as module; 
spoiler: does not work well enough).


CAVEAT: MUST BE FULLY REFACTORED



iface: the actual interface, which can be textual CLI or GUI

verbose: echo all log entries to terminal

filenamext: extension assumed for dataset files if absent

logfile: potential logging file

scale: for writing ints as floats with controlled precision loss

epsilon: to compare floats to zero, try to avoid using it

pend_len_limit: limit on the size of the heap of closures pending for expansion

pend_total_limit: max total length of info related to the pending closures

boostab: stability of boost, weight of current value 
 in front of lift values coming in

confthr: was about 2/3 for long, scaled; set at 0.6 for some
days, not convincing, settling for 0.65 for v1.1
(natural alternatives to consider: 3/4 and 4/5)

supp_rep_often: how often to report about the ongoing support - CONCEPT CHANGED

findrules: process bound, don't mine more than that many rules; 
 if zero or negative, don't apply any bound

maxrules: number of rules to be output, max boost among those found

initialboost: initial bound on the confidence boost

absoluteboost: NO WAY any rule reported has lower boost than that, EVER

genabsupp: Do not consider closures with absolute support below this

"""

# version = "version 1.2.2"
# ~ version = "1.2.5"

iface = None

# ~ very dirty trick to make implminer go
# ~ def put_iface_in_statics(the_iface):
    # ~ global iface
    # ~ iface = the_iface

# ~ filenamext = ".txt"
# ~ logfile = None
# ~ filename = None 
# ~ filenamefull = None

verbose = False

running = False

please_report = False # To report every now and then 
scale = 100000
epsilon = 100.0/scale
boostab = 5
supp_rep_often = 100 # every that many closures unless verbose
# report current support at most that many times # changed concept

## standard process:

pend_len_limit = 16384 # 1000 # 16384 # 2 to power 14
pend_total_limit = 100000000 # 100000 # 100000000
pend_mem_limit = 1000000000 # 1GB
##confthr = int((2.0/3) * scale)
confthr = int(0.65 * scale)
findrules = 0
maxrules = 50 # set this to zero if all the rules are to be written out
stdmaxrules = maxrules # to recover the standard situation if necessary
initialboost = 1.15
absoluteboost = 1.05
genabsupp = 5 # absolute number of transactions
boostdecr = 0.001 # minimal boost decrease allowed
report_period = 30 # try to show program is alive every that many seconds

# ~ def set_standard():
    # ~ "set to the same values as just indicated - guess it is not doing anything"
    # ~ pend_len_limit = 16384 
    # ~ pend_total_limit = 100000000
    # ~ pend_mem_limit = 1000000000
# ~ ##    confthr = int((2.0/3) * scale)
    # ~ confthr = int(0.65 * scale)
    # ~ findrules = 0
    # ~ maxrules = 50
    # ~ initialboost = 1.15
    # ~ absoluteboost = 1.05
    # ~ genabsupp = 5 

