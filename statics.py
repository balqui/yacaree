"""

Project: yacaree
Programmer: JLB

Module encompassing some static objects

datafilext: extension assumed for dataset files if absent

logfile: potential logging file

scale: for writing ints as floats with controlled precision loss

epsilon: to compare floats to zero, try to avoid using it

pend_limit: limit on the size of the heap of closures pending for expansion

pend_mem_limit: max amount of memory allowed for the pending closures

boostab: stability of boost, weight of current value in front of lift values coming in

confthr: about 2/3 for the moment, scaled
(natural alternatives to consider: 3/4 and 4/5)

supp_rep_often: how often to report about the ongoing support

maxrules: don't mine more than that many rules; if zero or negative, don't apply any bound

initialboost: initial bound on the confidence boost

absoluteboost: NO WAY any rule reported has lower boost than that, EVER

genabsupp: Do not consider closures with absolute support below this

FEATURES REMOVED (code commented out)

never: swallow three parameters and return False
(ToDo: make it swallow any number of parameters)

powset: iterator over all the subsets of the given set

"""

datafilext = ".txt"

logfile = None

scale = 100000

epsilon = 100.0/scale

pend_limit = 20000

pend_mem_limit = 500000000 # half a GB devoted to the pending closures heap

boostab = 5

confthr = int((2.0/3) * scale)

supp_rep_often = 25 # report current support at most 25 times

maxrules = 0

initialboost = 1.15

absoluteboost = 1.06

genabsupp = 5 # absolute number of transactions

##def never(n,s,t):
##    return False
##
##def powset(aset):
##    "iterator on the powerset of given aset"
##    if len(aset)==0:
##        yield set([])
##    else:
##        e = aset.pop()
##        for s in powset(aset):
##            s.add(e)
##            yield s
##            s.discard(e)
##            yield s

##closmemory = 1000000000 # 1GB for the Dell Latitude 4310 Win7
##closmemory = 500000000 # half a GB for testing
##closmemory = 100000000 # quite small for simple testing
##closmemory = 20000000 # very small for very simple testing
