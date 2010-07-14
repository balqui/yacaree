
import statics
from iface import iface
from itset import ItSet
from lattice import Lattice
from rule import Rule

from heapq import heapify, heappush, heappop
from collections import defaultdict

class yacareeMiner(Lattice):

    def __init__(self,datasetfilename):
        "some codes, reserved rules, and average lift so far"
        Lattice.__init__(self,datasetfilename)
        self.count = 0
        self.DISCARD = -1
##        self.RESERVE = -2
##        self.YIELD = 0
        self.reserved = []
        self.sumlifts = 0.0
        self.numlifts = 0

    def addlift(self,lft):
        self.sumlifts += lft
        self.numlifts += 1

    def meanlift(self):
        """
        mean lift so far of bisingleton rules seen
        used to drive a bit down the conf boost bound
        """
        return self.sumlifts / self.numlifts

    def checkrule(self,rul):
        belowconf = 0
        for an2 in self.allpreds(rul.an):
            "ToDo: refactor avoiding floats"
            cn2 = self.close(rul.rcn.union(an2))
            if float(self.supps[cn2])/self.supps[an2] > belowconf:
                belowconf = float(self.supps[cn2])/self.supps[an2]
            if float(rul.conf)/belowconf < statics.absoluteboost:
                return self.DISCARD
        if rul.cboo < statics.epsilon:
            "ToDo: refactor without floats"
            if rul.cn in self.suppratios:
                rul.cboo = self.suppratios[rul.cn]
            if belowconf > 0:
                if rul.cboo > rul.conf/belowconf or rul.cboo < statics.epsilon:
                    rul.cboo = rul.conf/belowconf
        return rul.cboo

    def minerules(self,safetysupp=0):
        "check boost wrt smaller antecedents only"
        for cn in self.candClosures(safetysupp):
            for an in self.allpreds(cn,(self.supps[cn]*statics.scale)/statics.confthr):
                rul = Rule(an,cn,self)
                if len(cn) == 2 and len(an) == 1:
                    "boost revision may require to fish back in reserved rules"
                    if rul.lift > 1:
                        self.addlift(rul.lift)
                        self.reviseboost(self.meanlift())
                        rereserved = []
                        while self.reserved:
                            (negs,rul2) = heappop(self.reserved)
                            if rul2.cboo < self.boosthr:
                                heappush(rereserved,(negs,rul2))
                            else:
                                self.count += 1
                                yield rul2
                        self.reserved = rereserved
                ch = self.checkrule(rul)
                if ch == self.DISCARD:
                    pass
                elif ch < self.boosthr:
                    heappush(self.reserved,(-rul.supp,rul))
                else:
                    self.count += 1
                    yield rul

if __name__=="__main__":

##    fnm = "pumsb_star" # add a safety support eg 0.6 to minerules
##    fnm = "adultrain"  # add a safety support eg 0.05 to minerules
##    fnm = "cestas20"
##    fnm = "cmc-recod2"
    
    ruleminer = yacareeMiner(fnm)
    for rul in ruleminer.minerules(0.05):
        iface.report(str(ruleminer.count) + "/ " + str(rul))
        ans = raw_input("More? (<CR> to finish) ")
        if len(ans)==0: break

    iface.report("Proposed " + str(ruleminer.count) + " rules.")
    iface.endreport()
## send ruleminer to garbage collector and recover free memory
##    ruleminer = None
    exit(11)
        