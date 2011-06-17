"""

Project: yacaree
Programmer: JLB

Module encompassing some static objects

filenamext: extension assumed for dataset files if absent

logfile: potential logging file

scale: for writing ints as floats with controlled precision loss

epsilon: to compare floats to zero, try to avoid using it

pend_len_limit: limit on the size of the heap of closures pending for expansion

pend_total_limit: max total length of info related to the pending closures

boostab: stability of boost, weight of current value 
 in front of lift values coming in

confthr: about 2/3 for the moment, scaled
(natural alternatives to consider: 3/4 and 4/5)

supp_rep_often: how often to report about the ongoing support

findrules: process bound, don't mine more than that many rules; 
 if zero or negative, don't apply any bound

maxrules: number of rules to be output, max boost among those found

initialboost: initial bound on the confidence boost

absoluteboost: NO WAY any rule reported has lower boost than that, EVER

genabsupp: Do not consider closures with absolute support below this

"""

filenamext = ".txt"
logfile = None
filename = None
filenamefull = None

scale = 100000
epsilon = 100.0/scale
boostab = 5
supp_rep_often = 10 # report current support at most that many times

## standard process:

pend_len_limit = 200 # 16384 # 2 to power 14
pend_total_limit = 100000000
pend_mem_limit = 1000000000 # 1GB
confthr = int((2.0/3) * scale)
findrules = 0
maxrules = 50 # set this to zero if all the rules are to be written out
initialboost = 1.15
absoluteboost = 1.05
genabsupp = 5 # absolute number of transactions

def set_standard():
    "set to the same values as just indicated"
    pend_len_limit = 16384 
    pend_total_limit = 100000000
    pend_mem_limit = 1000000000
    confthr = int((2.0/3) * scale)
    findrules = 0
    maxrules = 50
    initialboost = 1.15
    absoluteboost = 1.05
    genabsupp = 5 

