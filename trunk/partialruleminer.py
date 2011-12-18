
import statics
##from choose_iface import iface
##from itset import ItSet
##from lattice import Lattice
from rule import Rule

from heapq import heapify, heappush, heappop
##from collections import defaultdict

def checkrule(rul,rm):
    belowconf = 0
    la = rm.latt
    for an2 in la.allpreds(rul.an):
        "ToDo: refactor avoiding floats"
        cn2 = la.close(rul.rcn.union(an2))
        if float(la.supps[cn2])/la.supps[an2] > belowconf:
            belowconf = float(la.supps[cn2])/la.supps[an2]
        if float(rul.conf)/belowconf < statics.absoluteboost:
            return rm.DISCARD
    if rul.cboo < statics.epsilon:
        "ToDo: refactor without floats"
        if rul.cn in la.suppratios:
            rul.cboo = la.suppratios[rul.cn]
        if belowconf > 0:
            if rul.cboo > rul.conf/belowconf or rul.cboo < statics.epsilon:
                rul.cboo = rul.conf/belowconf
    return rul.cboo

## mine_partial_rules very close to minerules in yacaree 1.1
## needs refactoring

def mine_partial_rules(rminer,cn):
    "check boost wrt smaller antecedents only"
    for an in rminer.latt.allpreds(cn,(rminer.latt.supps[cn]*statics.scale)/statics.confthr):
        rul = Rule(an,cn,rminer.latt)
        if len(an) == 1: # and len(cn) == 2:
            "boost revision may require to fish back in reserved rules"
            if 1 < rul.lift < rminer.latt.boosthr:
                rminer.addlift(rul.lift)
                rminer.latt.reviseboost(rminer.sumlifts,rminer.numlifts)
                rereserved = []
                while rminer.reserved:
                    (negs,rul2) = heappop(rminer.reserved)
                    if rul2.cboo < rminer.latt.boosthr:
                        heappush(rereserved,(negs,rul2))
                    else:
                        rminer.count += 1
                        yield rul2
                rminer.reserved = rereserved
        ch = checkrule(rul,rminer)
        if ch == rminer.DISCARD:
            pass
        elif ch < rminer.latt.boosthr:
            heappush(rminer.reserved,(-rul.supp,rul))
        else:
            rminer.count += 1
            yield rul

