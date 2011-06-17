"""
Project: yacaree
Programmers: JLB

Its main method is the iterator that provides, one by one, in order of 
 decreasing support, all the closures for a given dataset and support bound

handle the neg border:
 find max non support
 allows us to set correct value to the support ratios of the maximal sets
 consider sending the neg border from this iterator and handling these
  issues in lattice

"""

##import sys
##
from math import floor ##, pow

import statics
from itset import ItSet
##from iface import iface
from choose_iface import iface
from dataset import Dataset
from yaflheap import FlHeap

class ClMiner:

    def __init__(self,dataset,supp=0):
        """
        may receive an external support bound in (0,1]
        otherwise, resort to statics.genabsupp - most often this is used
        self.intsupp is support scaled into int in (0,dataset.nrtr]
        initializes other quantities and finds closures of singletons
        """
        self.dataset = dataset
        if supp > 0:
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

        """find closures of singletons: each has
        support, contents, and set of supporting transactions
        """
        self.clos_singl = set([])
        for (s,it) in sorteduniv:
            if s < self.intsupp:
                "no items remain with supp at intsupp or more"
                self.maxitemnonsupp = s
                self.maxnonsupp = s
                break
            supportingset = self.dataset.occurncs[it]
            cl_node = (s, frozenset(self.dataset.inters(supportingset)),
                       frozenset(supportingset))
            self.clos_singl.add(cl_node)
        sorteduniv = None # return memory space to garbage collector

    def mineclosures(self):
        """
        iterator to mine closed sets
        report progress at report_supp, update it with report_supp_factor
        """
        report_supp_factor = pow(1.0/self.maxitemsupp, 
                                 1.0/statics.supp_rep_often)
        report_supp = floor(self.maxitemsupp*report_supp_factor)
##        not sure negbordsize is correctly computed this way - CHECK
##        self.negbordsize = self.dataset.nrits - cnt # singletons in neg border

        cnt_pend = len(self.clos_singl)
        iface.report(str(cnt_pend) + " singleton-based closures.")

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            yield (ItSet([]),self.dataset.nrtr)
            self.card += 1

##        iface.report("Combining singletons.")

        pend_clos = FlHeap() # will use default scheme for priority
        pend_clos.push(self.clos_singl)
        self.minsupp = self.dataset.nrtr
##        self.size_pend = self.pend_clos_size(pend_clos)
        while pend_clos.more():
            "extract largest-support closure and find subsequent ones"
## size tests moved to yaflheap.FlHeap.test_size()
##            if (self.cnt_pend > statics.pend_len_limit or
##                self.size_pend > statics.pend_total_limit or
##                self.pend_clos_size(pend_clos) > statics.pend_mem_limit):
##                "too large current pending heap, increase support - reconsider size_pend"
##                self.halve_pend_clos(pend_clos)
####                pend_clos.halve()
##                self.cnt_pend = len(self.pend_clos)
##                self.size_pend = self.pend_clos_size() # or bring from halve
            self.intsupp = pend_clos.test_size(self.intsupp)
            cl = pend_clos.pop()
##            self.cnt_pend -= 1
##            self.size_pend -= len(cl[1]) + len(cl[2]) + 1
##            spp = -cl[0]
            spp = cl[0]
            if spp < self.intsupp:
                "maybe intsupp has grown in the meantime (neg border)"
                break
            if spp < self.minsupp:
                self.minsupp = spp
            if spp < report_supp:
                "time to report progress"
##                self.size_pend = self.pend_clos_size()
                iface.report(str(self.card) +
                             " closures found so far; current support " +
                             str(spp) + ".")
                report_supp = floor(report_supp*report_supp_factor)
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
                        next_clos = frozenset(self.dataset.inters(supportset))
                        if (next_clos not in
                            [ cc[1] for cc in pend_clos.storage ]):
##                            self.cnt_pend += 1
                            cl_node = (len(supportset), next_clos,
                                       frozenset(supportset))
                            pend_clos.push([cl_node])
##                            self.size_pend += (1 + len(cl_node[1]) +
##                                               len(cl_node[2]))

    def to_percent(self,anyintsupp):
        """
        anyintsupp expected absolute int support bound
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places)
        role is only human communication
        """
        return (floor(statics.scale*anyintsupp*100.0/self.dataset.nrtr) /
                statics.scale)

##    def pend_clos_size(self,pend_clos):
##        "by memory size, should try to spare recomputing it so often"
##        m = sys.getsizeof(pend_clos)
##        for b in pend_clos:
##            m += (sys.getsizeof(b[0]) +
##                  sys.getsizeof(b[1]) +
##                  sys.getsizeof(b[2]))
##        return m

##    def pend_clos_size(self):
##        "by lengths, insufficient for dense or big datasets"
##        m = len(self.pend_clos)
##        for pend in self.pend_clos:
##            m += len(pend[1]) + len(pend[2])
##        return m

##    def halve_pend_clos(self):
##        """
##        too many closures pending expansion: raise
##        the support bound so that about half of the
##        pend_clos heap becomes discarded
##        """
##        lim = self.cnt_pend / 2
##        current_supp = self.dataset.nrtr + 1
##        current_supp_clos = []
##        new_pend_clos = []
##        new_cnt = 0
##        old_intsupp = self.intsupp
##        while self.pend_clos:
##            b = heappop(self.pend_clos)
##            new_cnt += 1
##            if new_cnt > lim: break
##            if -b[0] == current_supp:
##                current_supp_clos.append(b)
##            else:
##                self.intsupp = current_supp
##                current_supp = -b[0]
##                new_pend_clos.extend(current_supp_clos)
##                current_supp_clos = [b]
##        self.pend_clos = new_pend_clos
##        iface.report("Increased min support from " + str(old_intsupp) +
##                     (" (%2.3f%%) up to " % self.to_percent(old_intsupp)) + 
##                     str(self.intsupp) +
##                     (" (%2.3f%%)" % self.to_percent(self.intsupp)) + ".")
        
if __name__ == "__main__":
    
    fnm = "data/markbask" 

    iface.report("Module clminer running as test on file " + fnm + ".txt")
    
    miner = ClMiner(Dataset(fnm+".txt"),0.01)

    cnt = 0
    for e in miner.clos_singl:
        cnt += 1
        print cnt, "/", ItSet(e[1]), "with support", e[0]

    iface.report("Found " + str(cnt) + " closures of singletons.")
    iface.endreport()

    cnt = 0
    for e in miner.mineclosures():
        cnt += 1
        print cnt, "/", e[0], "with support", e[1]

##    iface.report("Found " + str(cnt) + " closures.")


