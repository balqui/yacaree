"""
yacaree

Current revision: early Pluviose 2025

Lattice based on Hasse edges, that is, 
list of immediate predecessors for each node

Programmers: JLB

iPred condition: 

x ∈ lc(z) if and only if
x ∩ (⋃y∈Y y) ⊆ z, where Y is the set of lower covers of z already found;


NEXT: CLEAN UP both commented-out lines and print statements,
and somehow think about the boosthr reduction (method reduceboost
here below) and the fishing back closures from the freezer.

To take the dicts away (e.g. suppratio) I have the problem
that the potential covers, intersections of ItSets with border 
sets, are NOT ItSets right now and I have no idea of their
supportsets or supports. Can I look this up somewhere? The
info IS there but is in the keys of dict's such as immpreds,
the frozenset suffices to access the value of the dict but
I want to access... the key!?!?!

Postponing decisions and accepting quite an inefficiency
penalty for now, I move on into a Lattice that is a defaultdict
of pairs, simplified ItSet with just contents and support
plus list of immediate predecessors, also simplified ItSet's.
Put these pairs into a new dataclass, here in the same file.
SHORTLY AFTER TOOK ALL THAT BACK.

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

CAVEAT: unclear whether pushing the suppratio constraint is not closing
access to other valid parts of the lattice. Currently there are multiple
paths to everywhere and not many such cases are likely to exist but when
ClMiner evolves into Troppus this might become noticeable. WELL NO PROBLEM,
the freezer is only for purpose of yielding closures to the miner but
the closures themselves remain in the lattice.

About the wrong suppratio at positive border: 
skipped at v1.0, v1.1 approximates it 
assuming minsupp for closures below thr but then supprt==1 too often
supprt = float(self.supps[st])/self.miner.minsupp
Plans to get their correct suppratio
out of the negative border - NOT THAT EASY! 
(and what if no neg border exists?)
tried 2 (a sort of infinity), then tried the absolute 
boost threshold supprt = statics.absoluteboost
so that only relevant in case the boost threshold really 
drops to the limit - both unconvincing
Got back for 1.2.1 to the same strategy as in 1.1
The formal solution is infinity due to the condition on
support in the formal definition of suppratio in the paper:
bigger sets will not be mined so the rules that would force
down the cboost due to suppratio will not be shown anyway.
"""

from heapq import heapify, heappush, heappop
from collections import defaultdict

from iface import IFace
from itset import ItSet
from dataset import Dataset
from clminer import ClMiner
##from border_v10 import Border

# ~ def inffloat(): # Hope to get rid of it soon
    # ~ "functional form for the suppratios defaultdict factory"
    # ~ return IFace.hpar.inffloat 

class Lattice(dict):
    """
    Lattice is mainly the ordered dict of closures with their
    predecessors. Keys are the frozenset of the contents
    (CAVEAT: might instead think of using the autoincr label?):
    then can be accessed from either the frozenset alone 
    (provided it is a closed set!) or the whole ItSet. 
    Values are pairs: whole ItSet to complete info from 
    frozenset of contents and list of predecessors. As now 
    dict ensures to keep arrival order, it is support order.

    Previous docstring from version 1.*:
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
        super().__init__(self)
        self.dataset = dataset
        # ~ self.closeds = []                   # replaced by self-dict
        # ~ self.supps = {}                     # repl by field in ItSet
        # ~ self.suppratios = defaultdict(inffloat) # ditto
        # ~ self.union_cover = defaultdict(set) # moved to local var
        # ~ self.immpreds = defaultdict(list)   # replaced by self-dict
        # ~ self.ready = []
        # ~ self.freezer = []
        self.boosthr = IFace.hpar.initialboost
        self.miner = None   # to access miner.minsupp later
        self.minsupp = None # among closures with known suppratio

    def candidate_closures(self, supp = -1):
        """
        supp == -1: use hpar.genabsupp;
        o/w, expected in [0, 1]: use it instead.
        Iterate over closures that reach that support 
        and support ratio above current value of boosthr.
        Relies on iterator from ClMiner.
        """
        ready = []
        freezer = []
        bord = set([])
        union_covers = defaultdict(set)
        self.miner = ClMiner(self.dataset, supp)
        miner = self.miner
        # ~ miner = ClMiner(self.dataset, supp)
        # ~ for itst in self.miner.mine_closures():
        for itst in miner.mine_closures():
            """
            Closures come in either nonincreasing support or 
            nondecreasing size, hence all subsets of each closure 
            come before it - needed for the closure op.
            As dict is now iterated in order of arrival, can dispose of
            closeds.
            suppratios undefined for maximal sets - what to do?
            first node in list is closure of empty set
            union_covers init is always empty 
            (can we make do with a single union_cover instead of a dict?)
            """
            print(" .... miner sent:", itst)
            supp = itst.supp
            # ~ node = frozenset(itst)
            # ~ node = itst
            self[frozenset(itst)] = (itst, list()) # repeated contents, unavoidable I guess
            # ~ self.closeds.append(itst) # TO BE REMOVED
            # ~ self.supps[itst] = supp
            # ~ for pot_cover, bord_elem in [ (itst.intersection(bord_elem), bord_elem) 
                               # ~ for bord_elem in bord ]:
                # ~ "seems that some of these intersections are repeated, no error since different union_cover - THE PAPER USES A SET"
            for pot_cover in set( frozenset(itst.intersection(bord_elem)) for bord_elem in bord ):
                pot_cover = self[pot_cover][0] # to complete it
                print(" ....... considering", pot_cover.fullstr())
                print(" ....... for", itst)
                print(" ....... as union_cover is", union_covers[pot_cover])
                print(" ....... comparing", itst.intersection(union_covers[pot_cover]), "with", pot_cover)
                if itst.intersection(union_covers[pot_cover]) <= pot_cover:
                    "this is the iPred condition"
                    print(" ....... found that", pot_cover.fullstr(), "is immpred of", itst.fullstr())
                    self[itst][1].append(pot_cover)
                    if not union_covers[pot_cover]:
                        "first successor of pot_cover: gives its suppratio"
                        pot_cover.suppratio = float(pot_cover.supp)/supp
                        # ~ self.suppratios[pot_cover] = supprat
                        if pot_cover.suppratio >= self.boosthr:
                            print(" ....... to ready:", pot_cover)
                            # ~ heappush(self.ready,(self.dataset.nrtr-self.supps[pot_cover],pot_cover))
                            # ~ heappush(ready,(self.dataset.nrtr-self.supps[pot_cover],pot_cover))
                            heappush(ready, pot_cover)
                            print(" .... ready:", ' '.join(str(e) for e in ready))
                        else:
                            """
                            Let it wait: pushing suppratio constraint"
                            """
                            print(" ....... to freezer:", pot_cover)
                            # ~ heappush(self.freezer,(-supprat,pot_cover))
                            heappush(freezer, (-pot_cover.suppratio, pot_cover))
                    union_covers[pot_cover].update(itst)
                    print(" ....... take from bord:", pot_cover)
                    bord.discard(pot_cover)
            print(" ....... add", itst.fullstr(), "to bord:", bord)
            bord.add(itst)

            # ~ while self.ready:
            while ready:
                """
                At this point we have the closures and their heaviest
                predecessor so suppratio correct, but lack other preds
                """
                # ~ yield heappop(self.ready)[1]
                self.minsupp = ready[0].supp
                yield heappop(ready)

        print("\n\n ....... now pending bord w/o suppratios")
        print(" ....... highest unreached supp:", supp - 1)
        for st in bord:
            print(" ......... yielding:", st, "suppratio bound:", st.supp, "/", supp - 1, "=", st.supp/(supp - 1))
            yield st

        print(" ....... freezer:", freezer)
        self.minsupp = miner.minsupp # for reporting at end

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
        pending = [ e for e in self[itst][1] if e.supp <= spbd ]
        handled = set(pending)
        while pending:
            p = pending.pop()
            yield p
            for q in self[p][1]:
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
            s += str(self[e][0]) + f" {self[e][0].suppratio:2.3f} " \
              + ' '.join(str(p) for p in self[e][1]) + "\n"
        return s

    def reviseboost(self, s, n):
        """
        current value weights as boostab of the lifts added up
        only to reduce it, and provided it does not get that low
        PLAN 2025: STOP DEPENDING ON LIFT AS IT REQUIRES COMPUTING
        CLOSURES OF CONSEQUENTS, COMPARE QUANTITY OF RULES PASSING
        THE CBOOST THRESHOLD WITH QUANTITY OF CLOSURES IN FREEZER
        NOT PASSING THE SUPPRATIO THRESHOLD.
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
                    (spprt,st) = heappop(self.freezer)
                    assert spprt == -st.suppratio
                    heappush(self.ready, st)
                else:
                    break


if __name__=="__main__":

    from filenames import FileNames
    from hyperparam import HyperParam

    def printclos(la, a):
        print("\nClosure: ", a, a.supp)
        print("imm preds:")
        for e in la[a][1]: print(e, ",") #,
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
    fnm = "../data/toy"
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
    for a in la.candidate_closures(0.2):
        "This had a 0.1 arg"
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



    
