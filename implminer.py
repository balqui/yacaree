
import statics
##from choose_iface import iface
from itset import ItSet
##from lattice import Lattice
from rule import Rule

##from heapq import heapify, heappush, heappop
from heapq import heappush
##from collections import defaultdict

from iter_subsets import all_proper_subsets
from hypergraph import hypergraph

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
        if float(rul.conf)/belowconf < statics.absoluteboost:
            return rminer.DISCARD
    if rul.cboo < statics.epsilon:
        "ToDo: refactor without floats"
        if rul.cn in rminer.latt.suppratios:
            rul.cboo = rminer.latt.suppratios[rul.cn]
        if belowconf > 0:
            if rul.cboo > rul.conf/belowconf or rul.cboo < statics.epsilon:
                rul.cboo = rul.conf/belowconf
    return rul.cboo

def mine_implications(rminer,cn):
    "cn closure of sufficient suppratio, find implications there"
    mingens = []
    for m in _faces(cn,rminer.latt.immpreds[cn]).transv().hyedges:
        mingens.append(ItSet(m))
    if len(cn) == len(mingens[0]):
        "o/w no rules as cn is a free set and its own unique mingen"
        pass
    else:
        for an in mingens:
            if an in rminer.latt.supps:
                print "ALREADY IN SUPPS", 
                print an, rminer.latt.supps[cn], rminer.latt.supps[an]
            else: 
                rminer.latt.supps[an] = rminer.latt.supps[cn]
                rul = Rule(an,cn,rminer.latt)
                ch = checkrule(rul,rminer)
                if ch == rminer.DISCARD:
                    pass
                elif ch < rminer.latt.boosthr:
                    heappush(rminer.reserved,(-rul.supp,rul))
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




