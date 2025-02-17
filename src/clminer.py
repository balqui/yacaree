"""
Current date: late Pluviose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Closure miner based on the Troppus algorithm.
"""


from iface import IFace
from itset import ItSet
from dataset import Dataset

from heapq import heapify, heappush, heappop


class ClMiner(dict):
    """
    Troppus-based miner. It is a dict from frozensets of itemsets 
    (closed or not) to their closing ItSet's. Has a mine_closures 
    generator of course to be called from Lattice.
    CAVEAT: At some point, the ItSet part in the Lattice
    dict is to be replaced by this one.
    """

    def __init__(self, dataset, supp=-1):
        super().__init__()
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        self.card = 0
        # ~ self.minsupp = 0


    def supp_adding(self, itst, nitt):
        """
        Find support of the result of adding nitt (new item) to itst.
        If necessary, compute supporting set for that. Store on self 
        if not there yet.
        Leave sets and closures in the dict even if their support is 
        zero, these are not useful but we don't want to test them again
        (but grab a lot of memory since their closure is all the items)
        """
        exact = False # matches maybe a transaction
        itst = frozenset(itst)
        itstadd = frozenset(itst.union(nitt))
        if itstadd in self:
            "supp of union is supp of its closure"
            return self[itstadd].supp
        if itst in self:
            "itstadd not in self but itst is, intersect support sets"
            supp = set(self[itst].supportset) & nitt.supportset
            clos = self.dataset.inters(supp)
        else:
            "need to compute support set on data"
            supp, exact = self.dataset.slow_supp(itstadd)
            if exact:
                "matched a transaction hence it is closed"
                clos = itstadd
            else:
                "intersect support sets"
                clos = self.dataset.inters(supp)
        clos = ItSet(clos, supp)
        self[itstadd] = clos
        return clos.supp


    def test_size(self, stdheap):
        """
        Similar to test_size in yaflheap, with the so-called ugly hack, 
        but now for a standard heap kept in a standard list; other
        than that, very close to version 1.*.
        Does not need to be a method of this class currently.
        """
        intsupp = 0 # return 0 if supp unchanged o/w return new supp
        if (count := len(stdheap)) > IFace.hpar.pend_len_limit:
            """
            Too many closures pending expansion: raise
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


    def mine_closures(self):

        closempty = set()
        sorteditems = list()

        for it in self.dataset.univ:
            if len(self.dataset.occurncs[it]) == self.dataset.nrtr:
                closempty.add(it)
            else:
                sorteditems.append(
                    ItSet([it], self.dataset.occurncs[it])
                )

        sorteditems.sort() # decr supp, item tie-break, see ItSet.__lt__

        closempty = ItSet(closempty, range(self.dataset.nrtr))
        pend_clos = [ closempty ]

        self.minsupp = self.dataset.nrtr
        while pend_clos and IFace.running:
            "Yield next closure and handle extensions."
            clos = heappop(pend_clos)
            pclos = set(clos)  # mutable copy of contents
            self[frozenset(pclos)] = clos
            self.card += 1
            yield clos
            if self.card % IFace.hpar.supp_rep_often == 0:
                "Report and consider raising support."
                IFace.report(
                  f"{self.card} closures traversed, " +
                  f"{len(pend_clos)} further closures pending; " +
                  f"current support {clos.supp}.")
                new_supp = self.test_size(pend_clos)
                if new_supp > self.intsupp:
                    "support bound grew, heap halved, report"
                    IFace.report(
                      f"Increasing min support from {self.intsupp} " +
                      f"({self.intsupp*100/self.dataset.nrtr:5.3f}%) " + 
                      f"up to {new_supp} " + 
                      f"({new_supp*100/self.dataset.nrtr:5.3f}%).")
                    self.intsupp = new_supp

            first_level = False  # unless we find otherwise later on
            mxsupp = 0
            for itt in sorteditems:
                (i,) = itt # extract the item in the singleton ItSet
                if first_level:
                    "set at previous loop: no further i can clear mxsupp"
                    break
                if i in pclos:
                    "remove this i as required for all future i's"
                    pclos.remove(i)
                else:
                    nst = pclos.copy() # copy to modify
                    sp = self.supp_adding(nst, itt)
                    if not pclos:
                        "nst a singleton: back down to singletons level"
                        first_level = True
                    if sp > mxsupp:
                        ncl = self[frozenset(nst.union(itt))]
                        for j in ncl:
                            jtt = ItSet({j}, self.dataset.occurncs[j])
                            if (j not in clos and
                               (itt.supp > jtt.supp or
                               (itt.supp == jtt.supp and i > j))):
                                break
                        else:
                            if sp > clos.supp:
                                break
                            elif sp > self.intsupp:
                                heappush(pend_clos, ncl)
                                mxsupp = sp


if __name__ == "__main__":

    from filenames import FileNames
    from hyperparam import HyperParam
    from time import time

    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

    # ~ miner = ClMiner(d, 0.084)
    # ~ miner = ClMiner(d, 0.75)
    # ~ miner = ClMiner(d, 3/24)
    miner = ClMiner(d)
    print("Int support:", miner.intsupp)
    lcl = list()
    for cl in miner.mine_closures():
        lcl.append(cl)
        # ~ print(cl)
    print("# cl", len(lcl), miner.card)
    # ~ print("In dict:")
    # ~ for fs in miner:
        # ~ if miner[fs].supp == 0:
            # ~ print(fs, miner[fs])


# Reporting and support increase fragments from V1.*, PROBABLY TO REMOVE
            # ~ new_supp = test_size(pend_clos)
            # ~ if new_supp > self.intsupp:
                # ~ "support bound grows, heap halved, report"
                # ~ IFace.report("Increasing min support from " +
                             # ~ str(self.intsupp) +
                             # ~ (" (%2.3f%%) up to " %
                              # ~ self.to_percent(self.intsupp)) +
                             # ~ str(new_supp) +
                             # ~ (" (%2.3f%%)" %
                              # ~ self.to_percent(new_supp)) + 
                            # ~ ".")
                # ~ IFace.hpar.please_report = True
                # ~ self.intsupp = new_supp
            # ~ if spp < self.intsupp:
                # ~ "maybe intsupp has grown in the meantime (neg border)"
                # ~ break
            # ~ if spp < self.minsupp:
                # ~ self.minsupp = spp
            # ~ if (IFace.hpar.verbose or IFace.hpar.please_report or 
                # ~ self.card % IFace.hpar.supp_rep_often == 0):
                # ~ IFace.hpar.please_report = False
                # ~ IFace.report(str(self.card) +
                            # ~ " closures traversed, " +
                               # ~ str(len(pend_clos)) + 
                            # ~ " further closures found so far; current support " +
                            # ~ str(spp) + ".")

