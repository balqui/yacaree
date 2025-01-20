"""
Package: lattice based on Hasse edges, that is, list of
immediate predecessors for each node

Programmers: JLB

Offers:
.very simple init
.construction from clminer - expect it to establish the following invariant:
 if x is a proper subset of y, then x comes before y in the list of closures
.compute all preds
.compute closure op / test whether closed
.to string

ToDo:

.handle negative border issues
.migrate the heaps into flheaps
.read it in from XML file, edges included
 xml filename should include in the name not the supp but the maxnonsupp
 get it from neg border and then glob files and pick the one with highest
 maxnonsupp that is below supp, if it exists, o/w must mine
 load only a part of the closures in the available file, if desired support
 is higher than in the file
"""

from heapq import heapify, heappush, heappop
from collections import defaultdict

from iface import IFace
from itset import ItSet
from dataset import Dataset
from clminer import ClMiner
##from border_v10 import Border

def inffloat():
    "infinite float for the suppratios defaultdict factory"
    return float("inf")

class Lattice:
    """
    Lattice implemented as explicit list of closures from clminer
    with a dict of closed immediate predecessors for each closure.
    Also iterator on the basis of support and support ratio.
    Closures expected ordered in the list by decreasing supports
    or increasing sizes
    union_cover is the union of all immediate successors seen so far

    URGENT: closeds UNNECESSARY SINCE 3.7 WHEN DICTS KEPT ORDER

    CAVEAT: Should we dispense with the supportset in ItSet's once
    they have been mined? Then we only need the supp but is the 
    rescued memory useful enough to spend that time (by our deletion 
    and by the garbage collector)?
    """

    def __init__(self, dataset):
        self.dataset = dataset
        self.closeds = []
        self.supps = {}
        self.suppratios = defaultdict(inffloat)
        self.union_cover = defaultdict(set)
        self.immpreds = defaultdict(list)
        self.ready = []
        self.freezer = []
        self.boosthr = IFace.hpar.initialboost
        self.miner = None

    def candidate_closures(self):
        """
        DO NOT CALL THIS METHOD TWICE
        (supp extra arg default 0? Think!)
        iterate over closures that reach support ratio
        above current value of boosthr
        and support above supp in [0,1] (?),
        default as indicated by statics.genabsupp (?)
        lie on iterator from ClMiner
        """
        bord = set([])
        self.miner = ClMiner(self.dataset) # supp extra?
        # ~ for (node,supp) in self.miner.mine_closures():
        for itst in self.miner.mine_closures():
            """
            closures come in either nonincreasing support or nondecreasing
            size, hence all subsets of each closure come before it - needed
            for the closure op
            if dict could be iterated in order of arrival, can dispose of
            closeds and use nodes instead
            suppratios undefined for maximal sets - do we need this?
            first node in list is closure of empty set
            union_cover init is always empty
            """
            print(" ....... border received:", itst, "of type", type(itst))
            supp = itst.supp
            node = frozenset(itst)
            self.closeds.append(node) # WRONG IF CALLED TWICE
            self.supps[node] = supp
            for pot_cover in [ node.intersection(bord_elem) 
                               for bord_elem in bord ]:
                if node.intersection(self.union_cover[pot_cover]) <= pot_cover:
                    self.immpreds[node].append(pot_cover)
                    if not self.union_cover[pot_cover]:
                        "first successor of pot_cover: gives supprat"
                        supprat = float(self.supps[pot_cover])/supp
                        self.suppratios[pot_cover] = supprat
                        if supprat >= self.boosthr:
                            print(" ....... to ready:", pot_cover)
                            heappush(self.ready,(self.dataset.nrtr-self.supps[pot_cover],pot_cover))
                        else:
                            """
                            Let it wait: pushing suppratio constraint"
                            """
                            print(" ....... to freezer:", pot_cover)
                            heappush(self.freezer,(-supprat,pot_cover))
                    self.union_cover[pot_cover].update(node)
                    print(" ....... take from bord:", pot_cover)
                    bord.discard(pot_cover)
            print(" ....... put in bord:", node)
            bord.add(node)

            while self.ready:
                """
                At this point we have the closures and their heaviest
                predecessor so suppratio correct, but lack other preds
                """
                yield heappop(self.ready)[1]

        print(" ....... now pending bord w/ wrong suppratios...")
        for st in bord:
            """
            there remain to yield the positive border (maximal sets) 
            wrong suppratio there, skipped at v1.0, v1.1 approximates it 
            assuming minsupp for closures below thr but then supprt==1 too often
            supprt = float(self.supps[st])/self.miner.minsupp
            next version of yacaree should get their correct suppratio
            out of the negative border - NOT THAT EASY! 
            (and what if no neg border exists?)
            tried 2 (a sort of infinity), then tried the absolute 
            boost threshold supprt = statics.absoluteboost
            so that only relevant in case the boost threshold really 
            drops to the limit - both unconvincing
            now getting back for 1.2.1 to the same strategy as in 1.1
            """
            supprt = float(self.supps[st])/self.miner.minsupp
            self.suppratios[st] = supprt
            if supprt >= self.boosthr:
                print(" ....... from bord to ready:", st)
                heappush(self.ready,(self.dataset.nrtr-self.supps[st],st))
            else:
                print(" ....... from bord to freezer:", st)
                heappush(self.freezer,(-supprt,st))
            
        print(" ....... yielding ready leftovers...")
        while self.ready:
            yield heappop(self.ready)[1]
        print(" ....... left over in freezer:", self.freezer)

    def allpreds(self,node,spbd=-1):
        """
        iterator for all predecessors, dfs
        uses a set to avoid dups
        only return preds of absolute support at most spbd, default return all
        """
        if spbd < 0:
            spbd = self.dataset.nrtr
        pending = [ e for e in self.immpreds[node] if self.supps[e] <= spbd ]
        handled = set(pending)
        while pending:
            p = pending.pop()
            yield p
            for q in self.immpreds[p]:
                if self.supps[q] <= spbd and q not in handled:
                    handled.add(q)
                    pending.append(q)

    def close(self,st):
        "closure of set st according to current closures list"
        fst = ItSet(st)
        if fst in self.immpreds:
            "fast to test with hash, little expense may save a lot"
            return fst
        for node in self.closeds:
            "linear search - risks being slow"
            if st <= node:
                "largest support closure containing st"
                break
        else:
            "should check that node is included in universe"
            node = ItSet(self.dataset.univ)
        return node

# ~ set2node undefined - luckily isclosed never called
    # ~ def isclosed(self,st):
        # ~ "test closedness of set st according to current closures"
        # ~ return set2node(st) in self.nodes

    def __str__(self):
        s = ""
        for e in sorted(self.closeds):
            s += str(e) + "\n"
        return s

    def reviseboost(self,s,n):
        """
        current value weights as boostab of the lifts added up
        only to reduce it, and provided it does not get that low
        """
        s = s + IFace.hpar.boostab*self.boosthr
        n = n + IFace.hpar.boostab
        v = float(s)/n
        if v < IFace.hpar.absoluteboost:
            v = IFace.hpar.absoluteboost
        if v <= self.boosthr - IFace.hpar.boostdecr:
            self.boosthr = v
            IFace.report(("Confidence boost bound reduced to %2.3f." % v)) 
            IFace.please_report = True
            while self.freezer:
                "fish back in closures that reach enough supp ratio now"
                if -self.freezer[0][0] > self.boosthr:
                    (spp,st) = heappop(self.freezer)
                    heappush(self.ready,(self.dataset.nrtr-self.supps[st],st))
                else:
                    break


if __name__=="__main__":

    from filenames import FileNames
    from hyperparam import HyperParam

    def printclos(la, a):
        print("\nClosure: ", a, la.supps[a])
        print("imm preds:")
        for e in la.immpreds[a]: print(e, ",") #,
        print()
        print("all preds:")
        for e in la.allpreds(a): print(e, ",") #,
        if a in la.suppratios:
            print("supp ratio:", la.suppratios[a])
        else:
            print("no supp ratio for", a)
        print("\n\n")

##    fnm = "lenses_recoded.txt"

    # ~ fnm = "data/e14"
    fnm = "data/toy"

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    
    la = Lattice(d)

    la.boosthr = 1 # SHORTCIRCUIT SUPPRATIO CONSTRAINT PUSH
    closlist = list()
    for a in la.candidate_closures():
        "This had a 0.1 arg"
        print("\n\nNew closure:")
        printclos(la, a)
        closlist.append(a)

    print("At end:")
    for a in closlist:
        printclos(la, a)

##    la.boosthr = 1.25
##    for e in la.candClosures():
##        print e, la.supps[e]
##        la.reviseboost(la.boosthr-0.03,1)



    
