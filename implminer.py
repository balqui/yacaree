'''
Before anything: reporting of hytra unavailability is on statics.iface
which does not work anymore, so this must run with hytra installed.


Current usage of heappush might compare Rule's if supports coincide
On the CPython version of Python2 this was harmless
Python 3 does not allow comparing Rule's until proper comparison is added
Quick and dirty solution is adding a global counter of things entering
the heap through heappush so that comparison never arrives to the
Rule's themselves
Probably a decent solution would come from using my own heaps
See also partialruleminer.py
'''


from iface import IFace as iface
# ~ import statics
from itset import ItSet
from rule import Rule

from iface import IFace

##from choose_iface import iface
##from lattice import Lattice

from heapq import heappush
##from heapq import heapify, heappush, heappop
##from collections import defaultdict

from iter_subsets import all_proper_subsets

old_hygr = False

try:
    from hytra import HyperGraph as hypergraph
    from hytra import transv_zero as transv
except ImportError:
    "take note to report it, but wait until statics.iface exists"
    old_hygr = True
    from hypergraph_old import hypergraph, transv_zero as transv

def warn_potential_deprecation():
    global old_hygr
    if old_hygr:
        "report at most once"
        old_hygr = False
        # ~ statics.iface.report("Could not import from module HyTra.")
        # ~ statics.iface.report("Please pip install hytra at some point.")
        # ~ statics.iface.report("Falling back on deprecated hypergraph_old code.")
        IFace.reportwarning("Could not import from module HyTra.")
        IFace.reportwarning("Please pip install hytra at some point.")
        IFace.reportwarning("Falling back on deprecated hypergraph_old code.")

heappushcnt = 0 # see above

def _faces(itst,listpred):
        "listpred immediate preds of itst - make hypergraph of differences"
        itst = set(itst)
        return hypergraph(itst,[ itst - e for e in listpred ])

def checkrule(rul,rminer):
    belowconf = 0
    cl_ants = set([])
    for an2 in all_proper_subsets(set(rul.an)):
        cl_ants.add(rminer.latt.close(an2))
    for an2 in cl_ants:
        "ToDo: refactor avoiding floats"
        cn2 = rminer.latt.close(rul.rcn.union(an2))
        if float(rminer.latt.supps[cn2])/rminer.latt.supps[an2] > belowconf:
            belowconf = float(rminer.latt.supps[cn2])/rminer.latt.supps[an2]
        if float(rul.conf)/belowconf < iface.hpar.absoluteboost:
            return rminer.DISCARD
    if rul.cboo < iface.hpar.epsilon:
        "ToDo: refactor without floats"
        if rul.cn in rminer.latt.suppratios:
            rul.cboo = rminer.latt.suppratios[rul.cn]
        if belowconf > 0:
            if rul.cboo > rul.conf/belowconf or rul.cboo < iface.hpar.epsilon:
                rul.cboo = rul.conf/belowconf
    return rul.cboo

def mine_implications(rminer,cn):
    "cn closure of sufficient suppratio, find implications there"
    warn_potential_deprecation()
    global heappushcnt
    mingens = []
    for m in transv(_faces(cn,rminer.latt.immpreds[cn])).hyedges:
        mingens.append(ItSet(m))
    if len(cn) == len(mingens[0]):
        "o/w no rules as cn is a free set and its own unique mingen"
        pass
    else:
        for an in mingens:
            if an in rminer.latt.supps:
                print("ALREADY IN SUPPS") #, 
                print(an, rminer.latt.supps[cn], rminer.latt.supps[an])
            else: 
                rminer.latt.supps[an] = rminer.latt.supps[cn]
                rul = Rule(an,cn,rminer.latt)
                ch = checkrule(rul,rminer)
                if ch == rminer.DISCARD:
                    pass
                elif ch < rminer.latt.boosthr:
                    heappushcnt += 1
                    heappush(rminer.reserved,(-rul.supp,heappushcnt,rul))
                else:
                    rminer.count += 1
                    yield rul


## in case the implication fails the boost thr, goes into rminer.reserved
## like all the others, and will be fished back in from the partial rule 
## miner if a decrease of the boost thr leads to it

## MAJOR REFACTORING needed: this to become a class keeping 
## the "reserved" rules, filling that heap by calling on the
## coming closure just as above, and updating the conf boost thr 
## on the basis of all rules - keeps the highest reserved cboost 
## and starts yielding upon decreases




