"""
Project: yacaree
Programmers: JLB

Its main method is the iterator that provides, one by one,
 in order of decreasing support, all the closures for a given
 dataset and support bound
 
handle the neg border:
 find max non support
 allows us to set correct value to the support ratios of the
  maximal sets
 consider sending the neg border from this iterator and
  handling these issues in lattice

"""

from math import floor

import statics
from itset import ItSet
from choose_iface import iface
from dataset import Dataset
from yaflheap import FlHeap

class ClMiner:

    def __init__(self,dataset,supp=-1):
        """
        may receive an external support bound in (0,1]
        otherwise, resort to statics.genabsupp - most often,
        this is used - usage is always "supp > intsupp"
        with a proper inequality
        self.intsupp is again the evolving support bound,
        scaled into int in [0,dataset.nrtr]
        initializes other quantities and finds closures of
        singletons
        """
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = statics.genabsupp
        self.supp_percent = self.to_percent(self.intsupp)
        self.card = 0
        self.negbordsize = 0
        self.maxnonsupp = 0
        self.maxitemnonsupp = 0
        self.minsupp = 0
        iface.report("Initializing singletons.")

        "pair up items with their support and sort them"
        sorteduniv = [ (len(self.dataset.occurncs[item]),item)
                       for item in self.dataset.univ ]
        sorteduniv = sorted(sorteduniv,reverse=True)
        self.maxitemsupp = sorteduniv[0][0]

        """
        find closures of singletons: each has
        support, contents, and set of supporting transactions
        """
        self.clos_singl = set([])
        for (s,it) in sorteduniv:
            if s <= self.intsupp:
                "no items remain with supp > intsupp"
                self.maxitemnonsupp = s
                self.maxnonsupp = s
                break
            supportingset = self.dataset.occurncs[it]
            cl_node = (s,
                       frozenset(self.dataset.inters(supportingset)),
                       frozenset(supportingset))
            self.clos_singl.add(cl_node)
        iface.report(str(len(self.clos_singl)) +
                     " singleton-based closures.")

    def mine_closures(self):
        """
        iterator to mine closed sets
        reporting progress made possible at each yield
        """

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            self.card += 1
            yield (ItSet([]),self.dataset.nrtr)

        pend_clos = FlHeap() 
        pend_clos.mpush(self.clos_singl)
        self.minsupp = self.dataset.nrtr
        while pend_clos.more():
            """
            extract largest-support closure and find subsequent ones,
            possibly after halving the heap through test_size(),
            in which case we got a higher value for the intsupp bound
            """
            new_supp = pend_clos.test_size()
            if new_supp > self.intsupp:
                "support bound grows, heap halved, report"
                iface.report("Increasing min support from " +
                             str(self.intsupp) +
                             (" (%2.3f%%) up to " %
                              self.to_percent(self.intsupp)) +
                             str(new_supp) +
                             (" (%2.3f%%)" %
                              self.to_percent(new_supp)) + ".")
                self.intsupp = new_supp
            cl = pend_clos.pop()
            spp = cl[0]
            if spp < self.intsupp:
                "maybe intsupp has grown in the meantime (neg border)"
                break
            if spp < self.minsupp:
                self.minsupp = spp
            iface.possibly_report(str(self.card) +
                         " closures traversed, " +
                         str(pend_clos.count) + 
                         " further closures found so far; current support " +
                         str(spp) + ".")
            self.card += 1
            yield (ItSet(cl[1]),spp)
            for ext in self.clos_singl:
                "try extending with freq closures of singletons"
                if not ext[1] <= cl[1]:
                    supportset = cl[2] & ext[2]
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        self.negbordsize += 1
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        "find closure and test duplicateness"
                        next_clos = frozenset(self.dataset.inters(supportset))
                        if (next_clos not in
                            [ cc[1][1] for cc in pend_clos.storage ]):
                            cl_node = (len(supportset), next_clos,
                                       frozenset(supportset))
                            pend_clos.push(cl_node)

    def to_percent(self,anyintsupp):
        """
        anyintsupp expected absolute int support bound,
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places);
        role is only human communication
        """
        return (floor(statics.scale*anyintsupp*100.0/self.dataset.nrtr) /
                statics.scale)
        
if __name__ == "__main__":

## This testing only works for iface_TEXT in choose_iface

##    fnm = "data/markbask"
##    supp = 0.0005 # half a transaction, that is, supp > 0: all
    
    fnm = "data/e13"
    supp = 1.0/14

##    fnm = "data/adultrain"

    iface.report("Module clminer running as test on file " + fnm + ".txt")

##    miner = ClMiner(Dataset(fnm+".txt"),supp)
    miner = ClMiner(Dataset(fnm+".txt"))

    cnt = 0
    for e in miner.clos_singl:
        cnt += 1
        iface.report(str(cnt) + "/ " + str(ItSet(e[1])) + "  s: " + str(e[0]))

    iface.report("Now computing all affordable closures.")

    cnt = 0
    for e in miner.mine_closures():
        cnt += 1
        last = e
        iface.report(str(cnt) + "/ " + str(e[0]) + "  s: " + str(e[1]))

    iface.report("Found " + str(cnt) + " closures.")
    iface.report("Last closure generated was " +
                 str(last[0]) + "  s: " +
                 str(last[1]) + ".")
    iface.endreport()


