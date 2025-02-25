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
        # ~ self.boosthr = IFace.hpar.initialboost
        self.miner = None   # to access miner.minsupp later
        self.minsupp = None # among closures with known suppratio

    def candidate_closures(self, supp = -1):
        """
        supp == -1: use hpar.genabsupp;
        o/w, expected in [0, 1]: use it instead.
        Iterate over closures that reach that support.
        """
        ready = []
        # ~ freezer = [] # FORGETTING ABOUT SUPPRATIOS BUT THEN WHEN IS IT READY?
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
            # ~ print(" .... miner sent:", itst)
            supp = itst.supp
            self[itst] = list()
            for pot_cover in set( 
              frozenset(itst.intersection(bord_elem)) 
              for bord_elem in bord ):
                pot_cover = self.miner[frozenset(pot_cover)] # complete it
                if itst.intersection(union_covers[pot_cover]) <= pot_cover:
                    "this is the iPred condition"
                    self[itst].append(pot_cover)
                    if not union_covers[pot_cover]:
                        "first successor of pot_cover: gives its suppratio"
                        pot_cover.suppratio = float(pot_cover.supp)/supp
                        # ~ if pot_cover.suppratio >= self.boosthr:
                        # NOT PUSHING ANYMORE THE suppratio CONSTRAINT
                        heappush(ready, pot_cover)
                    union_covers[pot_cover].update(itst)
                    bord.discard(pot_cover)
            bord.add(itst)

            # ~ while self.ready:
            # ~ print(" .... ready:", ' '.join(str(e) for e in ready))
            while ready:
                """
                At this point we have the closures and their heaviest
                predecessor so suppratio correct, but lack other preds
                """
                self.minsupp = ready[0].supp
                yield heappop(ready)

        print("\n\n ....... now pending bord w/o suppratios")
        print(" ....... highest unreached supp:", supp - 1)
        for st in bord:
            # ~ print(" ......... yielding:", st, "suppratio bound:", st.supp, "/", supp - 1, "=", end = ' ')
            # ~ if supp > 1: 
                # ~ print(st.supp/(supp - 1))
            # ~ else:
                # ~ print("inf")
            self.minsupp = st.supp
            yield st

        # ~ print(" ....... freezer:", freezer)
        # ~ self.minsupp = miner.minsupp # for reporting at end

        # ~ print(" ....... now pending bord w/ wrong suppratios...")
        # ~ for st in bord:
            # ~ """
            # ~ There remain to yield the positive border (maximal sets).
            # ~ Earlier versions still tried to split them into ready and
            # ~ freezer but freezing them due to an approximate suppratio
            # ~ does not fit the formal definition in the ToKD paper.
            # ~ """
            # ~ supprt = float(self.supps[st])/self.miner.minsupp
            # ~ self.suppratios[st] = supprt
            # ~ if supprt >= self.boosthr:
                # ~ print(" ....... from bord to ready:", st)
                # ~ heappush(self.ready,(self.dataset.nrtr-self.supps[st],st))
            # ~ else:
                # ~ print(" ....... from bord to freezer:", st)
                # ~ heappush(self.freezer,(-supprt,st))
            
        # ~ print(" ....... yielding ready leftovers...")
        # ~ while self.ready:
            # ~ yield heappop(self.ready)[1]
        # ~ print(" ....... left over in freezer:", self.freezer)

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

# ~ Make sure whether I really need it, then refactor and avoid closeds
    # ~ def close(self,st):
        # ~ "closure of set st according to current closures list"
        # ~ fst = ItSet(st)
        # ~ if fst in self.immpreds:
            # ~ "fast to test with hash, little expense may save a lot"
            # ~ return fst
        # ~ for node in self.closeds:
            # ~ "linear search - risks being slow"
            # ~ if st <= node:
                # ~ "largest support closure containing st"
                # ~ break
        # ~ else:
            # ~ "should check that node is included in universe"
            # ~ node = ItSet(self.dataset.univ)
        # ~ return node

# ~ set2node undefined - luckily isclosed never called
    # ~ def isclosed(self,st):
        # ~ "test closedness of set st according to current closures"
        # ~ return set2node(st) in self.nodes

    def __str__(self):
        s = ""
        for e in self:
            s += (str(self.miner[e]) + f" {self.miner[e].suppratio:2.3f} " 
              + ' '.join(str(p) for p in self[e]) + "\n")
        return s

    # ~ def reviseboost(self, s, n):
        # ~ """
        # ~ current value weights as boostab of the lifts added up
        # ~ only to reduce it, and provided it does not get that low
        # ~ PLAN 2025: STOP DEPENDING ON LIFT AS IT REQUIRES COMPUTING
        # ~ CLOSURES OF CONSEQUENTS, COMPARE QUANTITY OF RULES PASSING
        # ~ THE CBOOST THRESHOLD WITH QUANTITY OF CLOSURES IN FREEZER
        # ~ NOT PASSING THE SUPPRATIO THRESHOLD.
        # ~ """
        # ~ s = s + IFace.hpar.boostab*self.boosthr
        # ~ n = n + IFace.hpar.boostab
        # ~ v = float(s)/n
        # ~ if v < IFace.hpar.absoluteboost:
            # ~ v = IFace.hpar.absoluteboost
        # ~ if v <= self.boosthr - IFace.hpar.boostdecr:
            # ~ self.boosthr = v
            # ~ IFace.report(("Confidence boost bound reduced to %2.3f." % v)) 
            # ~ IFace.please_report = True
            # ~ while self.freezer:
                # ~ "fish back in closures that reach enough supp ratio now"
                # ~ if -self.freezer[0][0] > self.boosthr:
                    # ~ (spprt,st) = heappop(self.freezer)
                    # ~ assert spprt == -st.suppratio
                    # ~ heappush(self.ready, st)
                # ~ else:
                    # ~ break


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

##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    
    la = Lattice(d)

    # ~ la.boosthr = 1 # SHORTCIRCUIT SUPPRATIO CONSTRAINT PUSH
    closlist = list()
    for a in la.candidate_closures(0):
        print("\n\nNew closure:")
        printclos(la, a)
        closlist.append(a)

    print("At end:")
    for a in closlist:
        printclos(la, a)

    print(la)

##    la.boosthr = 1.25
##    for e in la.candClosures():
##        print e, la.supps[e]
##        la.reviseboost(la.boosthr-0.03,1)



    
