"""
Current date: late Pluviose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Conjoining the current clminer from refactored yacaree with the
code from troppus of old to try and get a working alternative.

Main method is the iterator that provides, one by one,
 in order of decreasing support, all the closures for a given
 dataset and support bound.
"""


from iface import IFace
from itset import ItSet
from dataset import Dataset

from heapq import heapify, heappush, heappop

def test_size(stdheap):
	"""
	Similar to test_size in yaflheap, probably with ugly hack, 
    but now for a standard heap kept in a standard list.
    CAVEAT: FULLY UNTESTED AS OF NOW.
	"""
	intsupp = 0
	if (count := len(stdheap)) > IFace.hpar.pend_len_limit:
		"""
		too many closures pending expansion: raise
		the support bound so that about half of the
		heap becomes discarded. Careful that support-tied
        ItSet's are either all kept or all discarded.
		"""
		lim = count // 2
		current_supp = stdheap[0].supp
		current_supp_clos = []
		new_pend_clos = []
		new_total_size = 0
		new_count = 0
		popped_count = 0
		while stdheap:
			itst = heappop(stdheap)
			popped_count += 1
			if popped_count > lim: break
			if itst.supp == current_supp:
				current_supp_clos.append(itst)
			else:
				current_supp = itst.supp
				intsupp = current_supp
				new_pend_clos.extend(current_supp_clos)
				current_supp_clos = [itst]
		stdheap = new_pend_clos
	return intsupp


class ClMiner_y:
    """
    refactored yacaree miner
    """

    def __init__(self, dataset, supp=-1):
        """
        May receive an external support bound in (0,1];
        otherwise, resorts to IFace.hpar.genabsupp 
        (most often, that is the case). 
        The evolving support bound is self.intsupp:
        supp scaled into int in [0, dataset.nrtr].
        Bound usage is always "supp > self.intsupp"
        with a proper inequality.
        Initializes other quantities and starts by 
        finding closures of singletons.
        CAVEAT: it finishes now yielding the positive border 
        but might one day complete the negative border too,
        so that the info for computing cboost is there.
        """
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        # ~ self.supp_percent = self.to_percent(self.intsupp) # CAN I GET RID OF THIS?
        self.card = 0
        # ~ self.negbordsize = 0
        self.minsupp = 0

    def _handle_singletons(self):
        """
        Pairs up items with their supports and returns the set of
        closures of singletons, conditioned to sufficient support,
        to be heapified later,
        """
        IFace.report("Initializing singletons.")
        self.maxitemsupp = 0
        self.maxnonsupp = 0
        self.maxitemnonsupp = 0

        clos_singl = set()
        for it in self.dataset.univ:
            """
            Find closures of singletons: as ItSet's so that each has 
            support, contents, and set of supporting transactions.
            CAVEAT: actually this process finds single-antecedent
            full implications and may result in implminer doing
            redundant work.
            """
            s = len(self.dataset.occurncs[it])
            self.maxitemsupp = max(self.maxitemsupp, s)
            if s <= self.intsupp:
                self.maxitemnonsupp = max(self.maxitemnonsupp, s)
            else:
                supportingset = self.dataset.occurncs[it]
                clos = ItSet(self.dataset.inters(supportingset), supportingset)
                clos_singl.add(clos)
        self.maxnonsupp = self.maxitemnonsupp # for now
        IFace.report(f"{len(clos_singl)} singleton-generated" + 
                     f" closures at support above {self.intsupp}.")
        return clos_singl

                # ~ print(" ==== closure of:", it, "below support;")

    def mine_closures(self):

        clos_singl = self._handle_singletons() # gives value to maxitemsupp

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            self.card += 1
            yield ItSet([], range(self.dataset.nrtr))

        pend_clos = list(clos_singl)
        heapify(pend_clos)

        self.minsupp = self.dataset.nrtr
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
                if not ext << cl and not cl << ext:
                    "'subset or eq' overrides lshift"
                    supportset = cl.supportset & ext.supportset
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        "unclear whether storing here would suffice to keep negbord"
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        "find closure and test duplicateness"
                        next_clos = ItSet(self.dataset.inters(supportset), supportset)
                        if next_clos not in pend_clos:
                            heappush(pend_clos, next_clos)

class ClMiner_t:
    """
    troppus miner under reconstruction
    """

    def __init__(self, dataset, supp=-1):
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        self.card = 0
        self.minsupp = 0


    def mine_closures(self):

        closempty = set()
        sorteditems = list()

        for it in self.dataset.univ:
            if len(self.dataset.occurncs[it]) == self.dataset.nrtr:
                closempty.add(it)
            else:
                sorteditems.append(it)

        closempty = ItSet(closempty, range(self.dataset.nrtr))
        pend_clos = [ closempty ]

        sorteditems.sort() # stability: item order if same support 
        sorteditems.sort(reverse = True, 
                    key = lambda it: len(self.dataset.occurncs[it]))

        # ~ print(" ==== closure of empty:", closempty)
        # ~ print(" ==== sorted rest:", sorteditems)
        # ~ for it in sorteditems: print(" ==== ", it, len(self.dataset.occurncs[it]))

        # ~ heapify(pend_clos)

        self.minsupp = self.dataset.nrtr
        while pend_clos and IFace.running:
            clos = heappop(pend_clos)
            yield clos
            first_level = False  # unless we find otherwise later on
            mxsupp = 0
            pclos = set(clos)  # mutable copy of closure
            # Iterating with reverse we start with highest support closure
            for i in sorteditems:
                # ~ print(" ==== ", i)
                if first_level:
                    "set at previous loop: no further i can clear mxsupp"
                    # ~ print(" ======== prev loop set firstlevel")
                    break
                if i in pclos:
                    "remove this i as required for all future i's"
                    pclos.remove(i)
                else:
                    nst = pclos.copy()  # copy to modify
                    nst.add(i)
                    # ~ print(" ==== nst", nst)
                    # ~ sp = self.d.count(nst)
                    # ncl = self.d.close(nst) # moved off
                    exact = False
                    transcontain = list()
                    for tr in self.dataset.transcns:
                        if nst <= self.dataset.transcns[tr]:
                            transcontain.append(tr)
                            if self.dataset.transcns[tr] <= nst:
                                exact = True
                    if not pclos:
                        "nst a singleton: back down to singletons level"
                        first_level = True
                    sp = len(transcontain)
                    # ~ print(" ==== nst sp vs mxsupp", sp, mxsupp)
                    if sp > mxsupp:
                        # ~ ncl = self.d.close(nst)  # bring here for improvement
                        if exact:
                            ncl = ItSet(nst, transcontain)
                        else:
                            ncl = ItSet(self.dataset.inters(transcontain), transcontain)
                        # ~ print(" ==== ncl, exact", ncl, exact)
                        for j in ncl:
                            # ~ print(" ======== in ncl:", j)                        
                            if (j not in clos and
                                    # ~ self.d.before((i,), (j,))):
                                (len(self.dataset.occurncs[i]) >
                                len(self.dataset.occurncs[j])) or 
                                (len(self.dataset.occurncs[i]) == 
                                len(self.dataset.occurncs[j]) and i > j)):
                                break
                        else:
                            # ~ print(" ======== all in ncl valid, sp, ncl.supp", sp, ncl.supp)                            
                            if sp > clos.supp:
                                break
                            elif sp > self.intsupp:
                                # ~ print(" ==== pushing", ncl)
                                heappush(pend_clos, ncl)
                                # ~ print(" ==== mxsupp from/to", mxsupp, sp)
                                mxsupp = sp

            



    # ~ def dec_supp_cl(self):
        # ~ while self.pend.more():
            # ~ clos = self.pend.pop()
            # ~ yield clos  # pair (support,closure)
            # ~ first_level = False  # unless we find otherwise later on
            # ~ mxsupp = 0
            # ~ pclos = [i for i in clos[1]]  # mutable copy of closure
            # ~ # Iterating with reverse we start with highest support closure
            # ~ for i in reversed(self.d.items):
                # ~ if first_level:
                    # ~ "set at previous loop: no further i can clear mxsupp"
                    # ~ break
                # ~ if i in pclos:
                    # ~ "remove this i as required for all future i's"
                    # ~ pclos.pop()
                # ~ else:
                    # ~ nst = pclos * 1  # copy to modify
                    # ~ nst.append(i)
                    # ~ sp = self.d.count(nst)
                    # ~ # ncl = self.d.close(nst) # moved off
                    # ~ if not pclos:
                        # ~ "nst a singleton: back down to singletons level"
                        # ~ first_level = True
                    # ~ if sp > mxsupp:
                        # ~ ncl = self.d.close(nst)  # bring here for improvement
                        # ~ for j in ncl:
                            # ~ if (j not in clos[1] and
                                    # ~ self.d.before((i,), (j,))):
                                # ~ break
                        # ~ else:
                            # ~ if sp > clos[0]:
                                # ~ break
                            # ~ else:
                                # ~ self.pend.push((sp, ncl))
                                # ~ mxsupp = sp


        # ~ print(" ==== closure of empty:", closempty)


if __name__ == "__main__":

    from filenames import FileNames
    from hyperparam import HyperParam

    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    fnm = "../data/adultrain"

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()
    m_t = ClMiner_t(d, 0.5)
    m_y = ClMiner_y(d, 0.5)
    
    # ~ miner = ClMiner(d, 0.084)
    # ~ miner = ClMiner(d, 0.75)
    # ~ miner = ClMiner(d, 3/24)
    # ~ miner = ClMiner(d)
    # ~ print(miner.intsupp)
    for cl in m_y.mine_closures():
        print(cl)
    for cl in m_t.mine_closures():
        print(cl)

