"""
Relies on implminer and partialruleminer for the actual mining.
Each of these needs its own different checkrule (with or without closures).
Here we keep the Lattice and the tracking of the boost threshold.
Also we call from here the main iterator in Lattice and run
each of implminer and partialruleminer on each closure.
Plan is to change this into two (or more?) separate processes (tricky).
"""


import statics
from choose_iface import iface
##from itset import ItSet
from lattice import Lattice
##from rule import Rule

##from heapq import heapify, heappush, heappop
##from collections import defaultdict

from implminer import mine_implications

from partialruleminer import mine_partial_rules

class RuleMiner: # Does not subclass Lattice anymore

    def __init__(self,datasetfilename):
        "some codes, reserved rules, and average lift so far"
        self.latt = Lattice(datasetfilename)
        self.count = 0
        self.DISCARD = -1
        self.reserved = []
        self.sumlifts = 0.0
        self.numlifts = 0

    def addlift(self,lft):
        self.sumlifts += lft
        self.numlifts += 1

    def minerules(self,safetysupp=0):
        for cn in self.latt.candidate_closures(): 
            "check that suppratio constraint already pushed"
            for rul in mine_implications(self,cn):
                yield rul
            for rul in mine_partial_rules(self,cn):
                yield rul

if __name__=="__main__":

##    fnm = "pumsb_star"
##    fnm = "cmc-full"
##    fnm = "adultrain"
    fnm = "e13"
    
    miner = RuleMiner(fnm)
    for rul in miner.minerules(0.05):
        iface.report(str(miner.count) + "/ " + str(rul))
        ans = iface.ask_input("More? (<CR> to finish) ")
        if len(ans)==0: break

    iface.report("Proposed " + str(miner.count) + " rules.")
    iface.endreport()

## send ruleminer to garbage collector and recover free memory
    ruleminer = None
    exit(0)

