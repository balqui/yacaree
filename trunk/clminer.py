"""
Project: yacaree - based on evolutions of slatt's clattice
Programmers: JLB

Iterator that provides, one by one, in order of 
 decreasing support, all the closures
 for a given dataset and support bound

check heapdict - min heapq from std lib requires sign change of supp

data in Dataset: univ, nrtr, nrits, nrocc

ToDo:

handle the neg border:
 gives max non support
 allows us to set correct value to the
 support ratios of the maximal sets
 consider sending the neg border from this iterator
 and handling these issues in lattice

xml in lattice, keep the Hasse edges (optionally maybe)

xml filename should include in the name not the supp but the maxnonsupp

get it from neg border and then glob files and pick the one with highest
maxnonsupp that is below supp, if it exists, o/w must mine

load only a part of the closures in the available file, if desired support
is higher than in the file

"""

from math import floor
from heapq import heapify, heappush, heappop

import statics
from itset import ItSet
from iface import iface
from dataset import Dataset

class ClMiner:
    """
    """

    def __init__(self,supp,dataset):
        """
        float supp in [0,1]; except if 0, means use statics.genabsupp 
        create closure space from dataset
        ToDo: read it in from clos file
        """
        self.dataset = dataset
        if supp == 0:
            "mild default bound"
            supp = statics.genabsupp
        self.intsupp = floor(supp * dataset.nrtr)
        self.supp_percent = self.topercent(self.intsupp)
        self.xmlfilename = "%s_cl%2.3fs.xml" % (dataset.filename,self.supp_percent)
        self.card = 0
        self.negbordsize = 0
        self.maxnonsupp = 0
        self.maxitemsupp = 0
        self.minsupp = 0

    def mineclosures(self):
        "no closures file, iterator must mine closed sets"
        clos_singl = set([])
        self.negbordsize = 0
        iface.report("Computing closures at support %3.2f%%;" %
                        self.topercent(self.intsupp)) 
        iface.say("initializing singletons...") # reserve to only very verbose
        self.maxitemsupp = 0
        self.maxnonsupp = 0
        for item in self.dataset.univ:
            "initialize (min-)heap with closures of singletons"
            iface.pong() # reserve to only verbose - no further pongs, take care of this upon using iterator
            supset = self.dataset.occurncs[item]
            supp = len(supset)
            if supp > self.maxitemsupp: self.maxitemsupp = supp
            if supp > self.intsupp:
                "probably very slow"
                clos_singl.add((self.dataset.nrtr-supp,
                                frozenset(self.dataset.inters(supset)),
                                frozenset(supset)))
            else:
                self.negbordsize += 1
                if supp > self.maxnonsupp:
                    self.maxnonsupp = supp
        cnt_clos_singl = len(clos_singl)
        iface.say(str(cnt_clos_singl) + " singleton-based closures.\n") # reserve to only very verbose
        if self.maxitemsupp < self.dataset.nrtr:
            "largest support on empty closure"
            yield (ItSet([]),self.dataset.nrtr)
            self.card += 1
        pend_clos = list(clos_singl.copy())
        heapify(pend_clos)
        self.minsupp = self.dataset.nrtr
        while pend_clos:
            "extract largest-support closure and find subsequent ones"
            cl = heappop(pend_clos)
            spp = self.dataset.nrtr - cl[0]
            self.card += 1
            yield (ItSet(cl[1]),spp)
            for ext in clos_singl:
                "try extending with freq closures of singletons"
                if not ext[1] <= cl[1]:
                    supportset = cl[2] & ext[2]
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        self.negbordsize += 1
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        if spp < self.minsupp:
                            self.minsupp = spp
                        next_clos = frozenset(self.dataset.inters(supportset))
                        if next_clos not in [ cc[1] for cc in pend_clos ]:
                            heappush(pend_clos, (self.dataset.nrtr-len(supportset),
                                     next_clos, frozenset(supportset)))

    def topercent(self,anyintsupp):
        """
        anyintsupp expected absolute int support bound
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places)
        """
        return floor(statics.scale*anyintsupp*100.0/self.dataset.nrtr)/statics.scale

if __name__=="__main__":

    support = 0.15
##    support = 0.5
##    fnm = "lenses_recoded"
    fnm = "e13"
##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    iface.report("Module clminer running as test on file " +
                 fnm + ".txt with support " + ("%2.3f%%" % support))
    
    miner = ClMiner(support,Dataset(fnm+".txt"))

    for e in miner.mineclosures():
        iface.say(str(e[0])+" ("+str(e[1])+")\n")


