"""
yacaree

Current revision: mid Pluviose 2025

Programmers: JLB

Previous version docstring:
Relies on implminer and partialruleminer for the actual mining.
Each of these needs its own different checkrule (with or without closures).
Here we keep the Lattice and the tracking of the boost threshold.
Also we call from here the main iterator in Lattice and run
each of implminer and partialruleminer on each closure.
Plan is to change this into two (or more?) separate processes (tricky).
"""


# ~ import statics
# ~ from choose_iface import iface
from iface import IFace
# ~ from iface import IFace as iface
##from itset import ItSet
from lattice import Lattice
from rule import Rule

##from heapq import heapify, heappush, heappop
##from collections import defaultdict

from implminer import mine_implications

from partialruleminer import mine_partial_rules

class RuleMiner: # Does not subclass Lattice anymore

    def __init__(self, hpar, dataset, supprat = True):
        "some codes, reserved rules, and average lift so far"
        self.latt = Lattice(dataset)
        if not supprat:
            self.latt.boosthr = 1 # SHORTCIRCUIT SUPPRATIO CONSTRAINT PUSH
        self.count = 0
        # ~ self.DISCARD = -1
        # ~ self.reserved = []
        # ~ self.sumlifts = 0.0
        # ~ self.numlifts = 0

    # ~ def addlift(self,lft):
        # ~ self.sumlifts += lft
        # ~ self.numlifts += 1

    def minerules(self, supp = -1):
        """
        supp == -1: use hpar.genabsupp;
        o/w, expected in [0, 1]: use it instead.
        Early version had an undocumented 'safetysupp' instead.
        """
        for cn in self.latt.candidate_closures(supp): 
            # ~ yield (cn, self.latt[cn])
            if cn:
                for rul in mine_implications(self.latt, cn):
                    self.count += 1
                    yield Rule(*rul, full_impl = True)
                for rul in mine_partial_rules(self, cn):
                    rul = Rule(*rul)
                    if rul.conf > IFace.hpar.confthr:
                        self.count += 1
                        yield rul
            else:
                print(" === skipping emptyset:", cn)

if __name__=="__main__":

    from hyperparam import HyperParam
    from filenames import FileNames
    from dataset import Dataset

##    fnm = "pumsb_star"
##    fnm = "cmc-full"
##    fnm = "adultrain"
    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    # ~ fnm = "../data/e5b"
    # ~ fnm = "../data/e5"
    fnm = "../data/p5.td"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"
    # ~ fnm = "../data/papersTr" # FILLS MEMORY ANYHOW EVEN WITH THE TOTAL SUPPORT SET LENGTHS LIMIT
    # ~ fnm = "../data/votesTr" 
    # The next work thanks to the limit on the total support set lengths
    # ~ fnm = "../data/chess.td"   # Fills memory with small heap size
    # ~ fnm = "../data/connect.td" # Fills memory with ridiculous heap
                                   # size and less than 5000 closures

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()
    
    # ~ miner = RuleMiner(fnm)
    miner = RuleMiner(IFace.hpar, d)
    for rul in miner.minerules(0):
        # ~ if rul.conf == 1:
        # ~ if rul.an == set(['a', 'b']):
        # ~ if len(rul.an) == 2 == len(rul.rcn):
            IFace.report(str(miner.count) + "/ " + str(rul))
        # ~ iface.report(str(miner.count) + "/ " + str(rul[0]) + " --> " + 
        # ~ str(rul[1]) +
        # ~ " c: " + str(rul[1].supp/rul[0].supp) )
        # ~ ans = iface.ask_input("More? (<CR> to finish) ")
        # ~ if len(ans)==0: break

    # ~ print("Lattice:")
    # ~ for a in miner.latt:
        # ~ print(a)

    # ~ iface.report("Proposed " + str(miner.count) + " rules.")
    # ~ iface.endreport()

## send ruleminer to garbage collector and recover free memory
    # ~ ruleminer = None
    # ~ exit(0)

