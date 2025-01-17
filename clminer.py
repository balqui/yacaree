"""
yacaree

Current revision: late Nivose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Main method is the iterator that provides, one by one,
 in order of decreasing support, all the closures for a given
 dataset and support bound.

Still pending: handle the neg border,
 find max non support
 set correct value to the support ratios of the
  maximal sets
 consider sending the neg border from this iterator and
  handling these issues in lattice


TOWARDS MAIN CHANGE IN 2025: INSTEAD OF CONSTRUCTING AN ItSet
TO YIELD WE STORE ALREADY ItSet's IN THE HEAP, SO AS TO USE
THE STANDARD heapq LIBRARY.
"""

from math import floor

from iface import IFace
from itset import ItSet
from dataset import Dataset
from yaflheap import FlHeap, test_size # test_size variant for standard lists

from heapq import heapify, heappush, heappop

class ClMiner:

    def __init__(self, dataset, supp=-1):
        """
        May receive an external support bound in (0,1];
        otherwise, resorts to IFace.hpar.genabsupp 
        (most often, that is the case). 
        The evolving support bound is self.intsupp,
        scaled into int in [0, dataset.nrtr].
        Bound usage is always "supp > self.intsupp"
        with a proper inequality.
        Initializes other quantities and starts by 
        finding closures of singletons.
        CAVEAT: it finishes now at the positive border
        but should complete the negative border too,
        so that the info for computing cboost is there.
        CAVEAT: A good part of this is not init material 
        but mineclosures material (initmine to be called
        from mineclosures once the heap is there)
        """
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        # ~ self.supp_percent = self.to_percent(self.intsupp) # CAN I GET RID OF THIS?
        self.card = 0
        self.negbordsize = 0
        self.minsupp = 0

    def _handle_singletons(self):
        """
        Pairs up items with their supports, sorts them, and
        initializes the heap with the closures of singletons 
        as ItSet's and returns it.
        CAVEAT: see if I can work directly on clos_singl and
        shortcircuit the usage of sorteduniv.
        """
        IFace.report("Initializing singletons.")
        sorteduniv = [ (len(self.dataset.occurncs[item]), item)
                       for item in self.dataset.univ ]
        sorteduniv = sorted(sorteduniv, reverse=True)
        # ~ self.maxitemsupp = sorteduniv[0][0]
        self.maxitemsupp = 0
        self.maxnonsupp = 0
        self.maxitemnonsupp = 0
        # ~ sortedunivalt = sorted([ ItSet([item], len(self.dataset.occurncs[item]))
                       # ~ for item in self.dataset.univ ])
        # ~ print(" ===== ", [str(s) for s in sortedunivalt], "(but need to close them!)")

        clos_singl = list()
        # ~ for (s, it) in sorteduniv:
        for it in self.dataset.univ:
            """
            Find closures of singletons: each has
            support, contents, and set of supporting transactions.
            CAVEAT: actually this process finds single-antecedent
            full implications and may result in implminer doing
            redundant work.
            CAVEAT: the first if/break discards part of the 
            negative border of the emptyset, hope that this
            is harmless, but think.
            """
            s = len(self.dataset.occurncs[it])
            self.maxitemsupp = max(self.maxitemsupp, s)
            if s <= self.intsupp:
                self.maxitemnonsupp = max(self.maxitemnonsupp, s)
                self.maxnonsupp = max(self.maxnonsupp, s)
                # ~ break # "no items remain with supp > intsupp NOT ANYMORE AS ITEMS TRAVERSED UNSORTED"
            supportingset = self.dataset.occurncs[it]
            clos = ItSet(self.dataset.inters(supportingset), supportingset)
            # ~ cl_node = (s,
                       # ~ frozenset(self.dataset.inters(supportingset)),
                       # ~ frozenset(supportingset))
            # ~ print(" ===== cl_node:", cl_node)
            if clos not in clos_singl:
                clos_singl.append(clos)
        IFace.report(str(len(clos_singl)) +
                     " singleton-based closures.")
        print(" ===== returned clos_singl", clos_singl)
        return clos_singl

        # ~ heapify(sortedunivalt)
        # ~ print(" ===== heap from sortedunivalt:", 
            # ~ [str(s) for s in sortedunivalt])


    def mine_closures(self):

        clos_singl = self._handle_singletons() # gives value to maxitemsupp

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            self.card += 1
            yield ItSet([], range(self.dataset.nrtr))

        # ~ pend_clos = FlHeap() 
        # ~ pend_clos.mpush(self.clos_singl)
        print(" ===== clos_singl:", [str(e) for e in clos_singl])
        pend_clos = clos_singl.copy()
        print(" ===== clos_singl.copy:", [str(e) for e in pend_clos])
        heapify(pend_clos)
        print(" ===== heapified:", [str(e) for e in pend_clos])
        print(" ===== clos_singl again:", [str(e) for e in clos_singl])
        # ~ pend_clos is now a heap on a standard list !!!
        self.minsupp = self.dataset.nrtr
        # ~ while pend_clos.more() and IFace.running:
        while pend_clos and IFace.running:
            """
            Extract largest-support closure and find subsequent ones,
            possibly after halving the heap through test_size(),
            in which case we got a higher value for the intsupp bound.
            """
            new_supp = test_size(pend_clos)
            if new_supp > self.intsupp:
                "support bound grows, heap halved, report"
                IFace.report("Increasing min support from " +
                             str(self.intsupp) +
                             (" (%2.3f%%) up to " %
                              self.to_percent(self.intsupp)) +
                             str(new_supp) +
                             (" (%2.3f%%)" %
                              self.to_percent(new_supp)) + 
                            ".")
                IFace.hpar.please_report = True
                self.intsupp = new_supp
            cl = heappop(pend_clos)
            print(" +++++ just popped:", cl)
            spp = cl.supp
            if spp < self.intsupp:
                "maybe intsupp has grown in the meantime (neg border)"
                break
            if spp < self.minsupp:
                self.minsupp = spp
            self.card += 1
            yield cl

            if (IFace.hpar.verbose or IFace.hpar.please_report or 
                self.card % IFace.hpar.supp_rep_often == 0):
                IFace.hpar.please_report = False
                IFace.report(str(self.card) +
                            " closures traversed, " +
                               str(pend_clos.count) + 
                            " further closures found so far; current support " +
                            str(spp) + ".")

            for ext in clos_singl:
                "try extending with freq closures of singletons"
                if (not set(ext) <= set(cl)
                and not set(cl) <= set(ext)):
                    print(" +++++ ext fires:", ext)
                    supportset = cl.supportset & ext.supportset
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        "unclear whether storing here would suffice to keep negbord"
                        self.negbordsize += 1
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        "find closure and test duplicateness"
                        next_clos = ItSet(self.dataset.inters(supportset), supportset)
                        if next_clos not in pend_clos:
                            heappush(pend_clos, next_clos)
                            print(" ===== heapified:", [str(e) for e in pend_clos])

    def to_percent(self, anyintsupp):
        """
        anyintsupp expected absolute int support bound,
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places);
        role is only human communication
        """
        return (floor(IFace.hpar.scale*anyintsupp*100.0/self.dataset.nrtr) /
                IFace.hpar.scale)
        
if __name__ == "__main__":

    from filenames import FileNames
    from hyperparam import HyperParam

    # ~ fnm = "data/lenses_recoded"
    fnm = "data/toy"
    # ~ fnm = "data/e13"
    # ~ fnm = "data/adultrain"

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()
    # ~ miner = ClMiner(d, 0.75)
    miner = ClMiner(d)
    for cl in miner.mine_closures():
        print(cl)

    # ~ tr_a = d.occurncs['a']
    # ~ tr_c = d.occurncs['c']
    # ~ tr_a = d.occurncs['Black']
    # ~ tr_c = d.occurncs['Doctorate']
    # ~ tr = tr_a & tr_c
    # ~ print(tr_a)
    # ~ print(tr_c)
    # ~ print(tr)
    # ~ print(d.inters(tr))

# ~ NEW TESTING PHASE TO BE REDESIGNED	

# ~ ## This testing only worked for iface_TEXT in choose_iface
# ~ ## Now that is being done differently and I must check it out

    # ~ from iface_TEXT import iface
    # ~ statics.iface = iface


# ~ ##    fnm = "data/markbask"
# ~ ##    supp = 0.0005 # half a transaction, that is, supp > 0: all
    
    # ~ fnm = "data/e13"
    # ~ supp = 1.0/14

# ~ ##    fnm = "data/adultrain"

    # ~ statics.iface.storefilename(fnm)
    # ~ statics.iface.report("Module clminer running as test on file " + fnm + ".txt")

# ~ ##    miner = ClMiner(Dataset(fnm+".txt"),supp)
    # ~ miner = ClMiner(Dataset(fnm+".txt"))

    # ~ cnt = 0
    # ~ for e in miner.clos_singl:
        # ~ cnt += 1
        # ~ statics.iface.report(str(cnt) + "/ " + str(ItSet(e[1])) + "  s: " + str(e[0]))

    # ~ statics.iface.report("Now computing all affordable closures.")

    # ~ cnt = 0
    # ~ for e in miner.mine_closures():
        # ~ cnt += 1
        # ~ last = e
        # ~ statics.iface.report(str(cnt) + "/ " + str(e[0]) + "  s: " + str(e[1]))

    # ~ statics.iface.report("Found " + str(cnt) + " closures.")
    # ~ statics.iface.report("Last closure generated was " +
                 # ~ str(last[0]) + "  s: " +
                 # ~ str(last[1]) + ".")
    # ~ ## statics.iface.endreport()


