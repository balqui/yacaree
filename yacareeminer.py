
import statics
from iface import iface
from itset import ItSet
from lattice import Lattice

from collections import defaultdict

class yacareeMiner(Lattice):
    "should be possible not to delve that deep - need a bound on allpreds"

    def __init__(self,datasetfilename):
        "rules: map conseq to antecs at the conf/cboost bounds"
        Lattice.__init__(self,datasetfilename)
        self.rules = defaultdict(list)
        self.sumlifts = 0.0
        self.numlifts = 0

    def addlift(self,lft):
        self.sumlifts += lft
        self.numlifts += 1

    def meanlift(self):
        return self.sumlifts / self.numlifts

    def lift(self,an,cn):
        "ToDo: refactor with strule"
        cnr = ItSet(cn.difference(an))
        sr = self.supps[self.close(cnr)]
        return float(self.supps[cn]*self.dataset.nrtr)/(self.supps[an]*sr)

    def minerules(self,safetysupp=0):
        "check boost wrt smaller antecedents only"
        for cn in self.candClosures(safetysupp):
            for an in self.allpreds(cn,(self.supps[cn]*statics.scale)/statics.confthr):
                cn2 = cn.difference(an)
                if len(cn) == 2 and len(an) == 1:
                    self.addlift(self.lift(an,cn))
                    print "BISINGLETON", self.strule(an,cn), "boost", self.boosthr, self.meanlift()
                    if self.meanlift() < self.boosthr:
                        self.reviseboost(self.meanlift())
                        iface.report("Current confidence boost bound: " +
                                     str(self.boosthr))
                discard_an = False
                for an2 in self.allpreds(an):
                    cn3 = self.close(cn2.union(an2))
                    if (self.supps[cn] * self.supps[an2] <
                        self.boosthr * self.supps[an] * self.supps[cn3]):
                        discard_an = True
                        break
                if not discard_an:
                    yield (an,cn)

    def strule(self,an,cn):
        san = self.supps[an]
        scn = self.supps[cn]
        cnr = ItSet(cn.difference(an))
        sr = self.supps[self.close(cnr)]
        cfd = "%2.3f" % (float(scn)/san)
        lft = "%2.3f" % self.lift(an,cn)
        spp = "%2.3f" % (float(scn)/self.dataset.nrtr)
        return ( str(an) + " => " + str(cnr) +
                 " [s:" + spp + ", c:" + cfd + ", l:" + lft + "]" )

if __name__=="__main__":

    fnm = "cestas20"
    
    ruleminer = yacareeMiner(fnm)

    for (an,cn) in ruleminer.minerules():
        iface.report(ruleminer.strule(an,cn))
        ans = raw_input("More? (<CR> to finish) ")
        if len(ans)==0: break

        