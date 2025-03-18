"""
yacaree

Current revision: early Ventose 2025

Lattice based on Hasse edges, that is, list of immediate 
predecessors for each node.
A dict that follows the support order of the closure miner.
However, be careful: right now, the local generator shuffles 
the order, due to waiting for the first superset to compute 
the support ratio, even though the support ratio constraint 
is not pushed anymore into the mining algorithm. CAVEAT: do
I need to change this?

Programmers: JLB

File with docstrings somewhere else, look it up some day.
"""

from heapq import heapify, heappush, heappop
from collections import defaultdict

from iface import IFace
from itset import ItSet
from dataset import Dataset
from clminer import ClMiner

class Lattice(dict):
    """
    Lattice is mainly the ordered dict of closures to their
    predecessor lists. Keys are (the frozenset of) the contents
    as follows from the definition of __hash__ in ItSet:
    then, can be accessed from either the frozenset alone 
    or the whole ItSet. 
    """

    def __init__(self, dataset):
        super().__init__(self)
        self.dataset = dataset
        self.minsupp = float("inf") # among closures with known suppratio

    def candidate_closures(self, supp = -1):
        """
        supp == -1: use hpar.genabsupp;
        o/w, expected in [0, 1]: use it instead.
        Iterate over closures that reach that support.
        """
        ready = []
        bord = set([])
        union_covers = defaultdict(set)
        self.miner = ClMiner(self.dataset, supp)
        for itst in self.miner.mine_closures():
            """
            Closures come in either nonincreasing support or 
            nondecreasing size, hence all subsets of each closure 
            come before it - needed for the closure op.
            Recall dict is now iterated in order of arrival.
            Pending to think about suppratios (undefined for maximals).
            union_covers init is always empty 
            (can we make do with a single union_cover instead of a dict?)
            """
            supp = itst.supp
            self[itst] = list()
            for pot_cover, b_elem in set( 
              (frozenset(itst.intersection(bord_elem)), bord_elem) 
              for bord_elem in bord ):
                if pot_cover == b_elem:
                    pot_cover_init = b_elem
                pot_cover = self.miner[frozenset(pot_cover)] # complete it - CAREFUL, CLOSES IT AS WELL
                if itst.intersection(union_covers[pot_cover]) <= pot_cover:
                    "this is the iPred condition"
                    self[itst].append(pot_cover)
                    if not union_covers[pot_cover]:
                        "first successor of pot_cover: gives its suppratio"
                        pot_cover.suppratio = float(pot_cover.supp)/supp
                        if pot_cover.suppratio >= IFace.hpar.abs_suppratio:
                            "Back to pushing up here the constraint"
                            assert pot_cover in self, \
                                f"{pot_cover} ready but not in lattice"
                            heappush(ready, pot_cover)
                    union_covers[pot_cover].update(itst)
                    bord.discard(pot_cover)
            bord.add(itst)

            while ready:
                """
                At this point we have the closures and their heaviest
                predecessor so suppratio correct, but lack other preds.
                The suppratio thing may lead to non-support-order!
                """
                self.minsupp = min(self.minsupp, ready[0].supp)
                yield heappop(ready)

        IFace.report("Lattice support border at: " + str(self.minsupp))
        IFace.report("Additional closures support border at: " + str(supp))

        # ~ for st in bord:
            # ~ "Positive border, maximal sets, no suppratio info, omitted"
            # ~ CAVEAT: THIS MAY BE PROVIDED 'ON REQUEST' BUT RIGHT NOW NO
            # ~ self.minsupp = st.supp
            # ~ yield st


    def allpreds(self, itst, spbd = -1):
        """
        iterator for all predecessors, dfs
        uses a set to avoid dups
        only return preds of absolute support at most spbd, 
        default return all
        """
        if spbd < 0:
            spbd = self.dataset.nrtr
        pending = [ e for e in self[itst] if e.supp <= spbd ]
        handled = set(pending)
        while pending:
            p = pending.pop()
            yield p
            for q in self[p]:
                if q.supp <= spbd and q not in handled:
                    handled.add(q)
                    pending.append(q)

    def __str__(self):
        s = ""
        for e in self:
            s += (str(self.miner[e]) + f" {self.miner[e].suppratio:2.3f} " 
              + ' '.join(str(p) for p in self[e]) + "\n")
        return s

if __name__=="__main__":

    from filenames import FileNames
    from hyperparam import HyperParam

    def printclos(la, a):
        print("\nClosure: ", a, a.supp)
        print("imm preds:")
        for e in la[a]: print(e, ",") #,
        print()
        print("all preds:")
        for e in la.allpreds(a): print(e, ",") #,
        print("supp ratio:", a.suppratio)
        # ~ if a in la.suppratios:
            # ~ print("supp ratio:", la.suppratios[a])
        # ~ else:
            # ~ print("no supp ratio for", a)
        print("\n\n")

    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e5b"
    fnm = "../data/p5.td"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/lenses_recoded.txt"

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

    la = Lattice(d)

    closlist = list()
    for a in la.candidate_closures(0):
        print("\n\nNew closure:")
        printclos(la, a)
        closlist.append(a)

    print("At end:")
    for a in closlist:
        printclos(la, a)

    print(la)
