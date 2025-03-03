"""
yacaree

Current revision: early Ventose 2025

Programmers: JLB

Right now it just goes through all the subsets of each closure 
and gives the pair as antecedent and consequent, not even confidence
is bounded.

REMEMBER THAT THE BELL IN IFACE HAS BEEN DEACTIVATED WHILE I REWORK OUT HYTRA


Previous version docstring:

Current usage of heappush might compare Rule's if supports coincide
On the CPython version of Python2 this was harmless
Python 3 does not allow comparing Rule's until proper comparison is added
Quick and dirty solution is adding a global counter of things entering
the heap through heappush so that comparison never arrives to the
Rule's themselves
Probably a decent solution would come from using my own heaps
See also implminer.py
"""


# ~ import statics
# ~ from iface import IFace as iface
##from choose_iface import iface
##from itset import ItSet
##from lattice import Lattice
from rule import Rule

# ~ from heapq import heapify, heappush, heappop
##from collections import defaultdict

from iface import IFace
from math import isfinite

# ~ heappushcnt = 0 # see above

DISCARD = -1

def checkrule(rul, rm):
    "Assumed a partial rule so both sides are closures"
    la = rm.latt
    nrtr = IFace.hpar.nrtr
    cn2 = la.miner.close(rul.rcn) # empty set gives cn2 closure of rcn, CAVEAT: CHECK OUT
    rul.lift = rul.an.supp * cn2.supp / rul.cn.supp * nrtr
    rul.levg = rul.an.supp * cn2.supp - rul.cn.supp * nrtr
    if isfinite(rul.cn.suppratio):
        rul.cboo = rul.cn.suppratio # initial upper bound
        if rul.cboo < IFace.hpar.absoluteboost:
            return DISCARD
        other_conf = rul.cn.suppratio
    else:
        other_conf = 0 # WRONG INITIALIZATION, MAY REACH THE FINAL DIVISION
    for an2 in la.allpreds(rul.an):
        "if empty set reached, fast, as already computed"
        cn2 = la.miner.close(rul.rcn.union(an2))
        if (cf := cn2.supp/an2.supp) > other_conf:
            other_conf = cf
        if rul.conf < IFace.hpar.absoluteboost * other_conf:
            rul.cboo = other_conf # only an upper bound but discarded
            return DISCARD
    rul.cboo = rul.conf/other_conf # not discarded, correct value
    return rul.cboo

    # ~ if rul.cboo < iface.hpar.epsilon:
        # ~ "ToDo: refactor without floats"
        # ~ if rul.cn in la.suppratios:
            # ~ rul.cboo = la.suppratios[rul.cn]
        # ~ if belowconf > 0:
            # ~ if rul.cboo > rul.conf/belowconf or rul.cboo < iface.hpar.epsilon:
                # ~ rul.cboo = rul.conf/belowconf

## mine_partial_rules very close to minerules in yacaree 1.1
## needs refactoring

def mine_partial_rules(rminer, cn):
    "check boost wrt smaller antecedents only"
    # ~ global heappushcnt
    for an in rminer.latt.allpreds(cn): #,(rminer.latt.supps[cn]*iface.hpar.scale)/iface.hpar.confthr):
        rul = Rule(an, cn) # ,rminer.latt)
        # ~ if len(an) == 1: # and len(cn) == 2:
            # ~ "boost revision may require to fish back in reserved rules"
            # ~ if 1 < rul.lift < rminer.latt.boosthr:
                # ~ rminer.addlift(rul.lift)
                # ~ rminer.latt.reviseboost(rminer.sumlifts,rminer.numlifts)
                # ~ rereserved = []
                # ~ while rminer.reserved:
                    # ~ (negs,_,rul2) = heappop(rminer.reserved) # for _ see implminer
                    # ~ if rul2.cboo < rminer.latt.boosthr:
                        # ~ heappushcnt -= 1
                        # ~ heappush(rereserved,(negs,heappushcnt,rul2))
                    # ~ else:
                        # ~ rminer.count += 1
                        # ~ yield rul2
                # ~ rminer.reserved = rereserved
        ch = checkrule(rul, rminer)
        print(" ..... just checked", rul)
        if ch == DISCARD:
            print(" ..... discarding", rul, ", low upper cboost bound")
            pass
        # ~ elif ch < rminer.latt.boosthr:
            # ~ heappushcnt -= 1
            # ~ heappush(rminer.reserved,(-rul.supp,heappushcnt,rul))
        else:
            # ~ yield (an, cn)
            yield rul

