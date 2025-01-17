'''
Current usage of heappush might compare Rule's if supports coincide
On the CPython version of Python2 this was harmless
Python 3 does not allow comparing Rule's until proper comparison is added
Quick and dirty solution is adding a global counter of things entering
the heap through heappush so that comparison never arrives to the
Rule's themselves
Probably a decent solution would come from using my own heaps
See also implminer.py
'''



# ~ import statics
from iface import IFace as iface
##from choose_iface import iface
##from itset import ItSet
##from lattice import Lattice
from rule import Rule

from heapq import heapify, heappush, heappop
##from collections import defaultdict


heappushcnt = 0 # see above

def checkrule(rul,rm):
    belowconf = 0
    la = rm.latt
    for an2 in la.allpreds(rul.an):
        "ToDo: refactor avoiding floats"
        cn2 = la.close(rul.rcn.union(an2))
        if float(la.supps[cn2])/la.supps[an2] > belowconf:
            belowconf = float(la.supps[cn2])/la.supps[an2]
        if float(rul.conf)/belowconf < iface.hpar.absoluteboost:
            return rm.DISCARD
    if rul.cboo < iface.hpar.epsilon:
        "ToDo: refactor without floats"
        if rul.cn in la.suppratios:
            rul.cboo = la.suppratios[rul.cn]
        if belowconf > 0:
            if rul.cboo > rul.conf/belowconf or rul.cboo < iface.hpar.epsilon:
                rul.cboo = rul.conf/belowconf
    return rul.cboo

## mine_partial_rules very close to minerules in yacaree 1.1
## needs refactoring

def mine_partial_rules(rminer,cn):
    "check boost wrt smaller antecedents only"
    global heappushcnt
    for an in rminer.latt.allpreds(cn,(rminer.latt.supps[cn]*iface.hpar.scale)/iface.hpar.confthr):
        rul = Rule(an,cn) # ,rminer.latt)
        if len(an) == 1: # and len(cn) == 2:
            "boost revision may require to fish back in reserved rules"
            if 1 < rul.lift < rminer.latt.boosthr:
                rminer.addlift(rul.lift)
                rminer.latt.reviseboost(rminer.sumlifts,rminer.numlifts)
                rereserved = []
                while rminer.reserved:
                    (negs,_,rul2) = heappop(rminer.reserved) # for _ see implminer
                    if rul2.cboo < rminer.latt.boosthr:
                        heappushcnt -= 1
                        heappush(rereserved,(negs,heappushcnt,rul2))
                    else:
                        rminer.count += 1
                        yield rul2
                rminer.reserved = rereserved
        ch = checkrule(rul,rminer)
        if ch == rminer.DISCARD:
            pass
        elif ch < rminer.latt.boosthr:
            heappushcnt -= 1
            heappush(rminer.reserved,(-rul.supp,heappushcnt,rul))
        else:
            rminer.count += 1
            yield rul

