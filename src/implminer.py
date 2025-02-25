'''
yacaree

Current revision: early Ventose 2025

Programmers: JLB

CAVEAT: As of today it constructs the Pasquier basis, not the GD.

Warns if TyTra unavailable, falls back to old transversal code; 
CAVEAT: HyTra untested for many years.





Earlier docstrings to revise:

VERY UGLY INHERITED HACKS

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


in mine_implications(latt, cn):
    
    cn closure of sufficient suppratio, find implications there but:
    - mingens of length 1 are replicating work from the clausures of 
    singletons
    - if all supersets below minsupp, suppratio not known, closure 
    does not make it to here
    - if all supersets with low supp even if some above minsupp.
    closure may take loooong to make it to here and others with
    smaller support may be seen before

Additional comment:

 in case the implication fails the boost thr, goes into rminer.reserved
 like all the others, and will be fished back in from the partial rule 
 miner if a decrease of the boost thr leads to it

 MAJOR REFACTORING needed: this to become a class keeping 
 the "reserved" rules, filling that heap by calling on the
 coming closure just as above, and updating the conf boost thr 
 on the basis of all rules - keeps the highest reserved cboost 
 and starts yielding upon decreases

'''


from iface import IFace as iface
# ~ import statics
from itset import ItSet
# ~ from rule import Rule

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

# ~ heappushcnt = 0 # see above

def _faces(itst, listpred):
        "listpred immediate preds of itst - make hypergraph of differences"
        # ~ itst = set(itst)
        return hypergraph(itst, [ itst.difference(e) for e in listpred ])

# ~ def checkrule(rul,rminer):
    # ~ belowconf = 0
    # ~ cl_ants = set([])
    # ~ for an2 in all_proper_subsets(set(rul.an)):
        # ~ cl_ants.add(rminer.latt.close(an2))
    # ~ for an2 in cl_ants:
        # ~ "ToDo: refactor avoiding floats"
        # ~ cn2 = rminer.latt.close(rul.rcn.union(an2))
        # ~ if float(rminer.latt.supps[cn2])/rminer.latt.supps[an2] > belowconf:
            # ~ belowconf = float(rminer.latt.supps[cn2])/rminer.latt.supps[an2]
        # ~ if float(rul.conf)/belowconf < iface.hpar.absoluteboost:
            # ~ return rminer.DISCARD
    # ~ if rul.cboo < iface.hpar.epsilon:
        # ~ "ToDo: refactor without floats"
        # ~ if rul.cn in rminer.latt.suppratios:
            # ~ rul.cboo = rminer.latt.suppratios[rul.cn]
        # ~ if belowconf > 0:
            # ~ if rul.cboo > rul.conf/belowconf or rul.cboo < iface.hpar.epsilon:
                # ~ rul.cboo = rul.conf/belowconf
    # ~ return rul.cboo

def is_cboost_high_impl(rul, latt):
    "rul assumed to be an implication, test std (non-closure) cboost"
    if rul.conf < 1:
        print(" .. test expected implication but got", rul)
        exit(1)
    print(" .. testing", rul)
    print(" .. type of consequent", type(rul.cn)) # should be always ItSet
    if rul.cn.suppratio < IFace.hpar.absoluteboost:
        print(" .. no, low suppratio")
        return False
    else:
        for it in rul.an:
            if confidence_of_an_minus_it_to_cn > 1/IFace.hpar.absoluteboost:
                print(" .. no, high conf taking out", it)
                return False
    return True

def mine_implications(latt, cn):
    """
    Gets a closure cn, with suppratio if known: find implications there.
    If all supersets below minsupp, suppratio not known.
    """
    warn_potential_deprecation()
    # ~ global heappushcnt
    # ~ mingens = []
    # ~ for m in transv(_faces(cn, latt[cn])).hyedges:
        # ~ mingens.append(ItSet(m))
        # ~ Maybe don't need it in Itset form yet
        # ~ but need to compute them first to check for free sets;
        # ~ hyedges is actually a list but this might change
    # ~ print(" == search for mingens of", cn)
    mingens = list( m for m in transv(_faces(cn, latt[cn])).hyedges )
    # ~ print(" == mingens of", cn, ":", mingens)
    if not mingens:
        print(" == No mingens:", cn, latt[cn])
    if len(cn) == len(mingens[0]):
        "o/w no rules as cn is a free set and its own unique mingen"
        pass
    else:
        for an in mingens:
            # ~ print(" == making a rule out of", an, "and", latt[cn])
            an = frozenset(an)
            if an in latt:
                print(an, "ALREADY IN lattice, then something wrong I believe")
                exit(1)
            else: 
                # ~ rminer.latt.supps[an] = rminer.latt.supps[cn]
                # ~ rul = Rule(an,cn,rminer.latt)
                # ~ ch = checkrule(rul,rminer)
                # ~ if ch == rminer.DISCARD:
                    # ~ pass
                # ~ elif ch < rminer.latt.boosthr:
                    # ~ heappushcnt += 1
                    # ~ heappush(rminer.reserved,(-rul.supp,heappushcnt,rul))
                # ~ else:
                    # ~ rminer.count += 1
                    # ~ yield rul
                    # ~ yield (set(an), set(cn))
                    yield (an, cn) # REMEMBER, cn is an ItSet but an just a frozenset






if __name__=="__main__":

    from filenames import FileNames
    from hyperparam import HyperParam
    from lattice import Lattice
    from dataset import Dataset

    fnm = "../data/e13"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/lenses_recoded.txt"


    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

    la = Lattice(d)
    supp = 0
    impls = list()

    for cn in la.candidate_closures(supp): 
        if cn:
            for rul in mine_implications(la, cn):
                impls.append(rul)
    if input(f"Show {len(impls)} implications? "):
        for rul in impls:
            print(rul[0], "=>", rul[1].difference(rul[0]))

    print("Lattice:")
    for a in la:
        print(a)

