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

.read it in from XML file, edges included
"""

import statics
from iface import iface
from itset import ItSet
from dataset import Dataset
from clminer import ClMiner
from border import Border
##from corr import corr

from heapq import heapify, heappush, heappop
from collections import defaultdict

class Lattice:
    """
    Lattice implemented as explicit list of closures from clminer
    with a dict of closed immediate predecessors for each closure
    from border
    Also iterator on the basis of support and support ratio
    Closures expected ordered in the list by decreasing supports
    or increasing sizes
    Compute also some minimal antecedents
    """

    def __init__(self,datasetfilename):
        "float supp in [0,1], hardwired confidence thr"
        self.closeds = []
        self.supps = {}
        self.suppratios = {}
        self.allbasics = {}
        self.immpreds = defaultdict(list)
        self.ready = []
        self.freezer = []
        self.dataset = Dataset(datasetfilename)
        self.boosthr = 1.3

    def candClosures(self,supp=0):
        """
        iterate over closures that reach support ratio
        above current value of boosthr
        and support above supp, default no pruning
        keep in prevcands closures already considered to avoid dup
        lie on iterator from ClMiner
        """
        prevcands = set([])
        miner = ClMiner(supp,self.dataset)
        bord = Border()
        for (node,supp) in miner.mineclosures():
            """
            set up preds and everything;
            closures come in either nonincreasing support or nondecreasing
            size, hence all subsets of each closure come before it - needed
            for the closure op
            if dict could be iterated in order of arrival, can dispose of
            closeds and use nodes instead
            suppratios undefined for maximal sets - do we need this?
            """
            iface.pong()
            self.closeds.append(node)
            self.supps[node] = supp
            self.immpreds[node] = bord.cover_update(node,self)
            bord.append(node)
            for pr in self.immpreds[node]:
                if pr in prevcands:
                    continue
                prevcands.add(pr)
                supprt = float(self.supps[pr])/supp
                self.suppratios[pr] = supprt
                if supprt > self.boosthr:
                    heappush(self.ready,(self.dataset.nrtr-self.supps[pr],pr))
                else:
                    heappush(self.freezer,(-supprt,pr))
            while self.ready:
                yield heappop(self.ready)[1]
        for st in bord.contents:
            "there remain to yield the maximal sets"
            heappush(self.ready,(self.dataset.nrtr-self.supps[st],st))
        while self.ready:
            yield heappop(self.ready)[1]

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

    def isclosed(self,st):
        "test closedness of set st according to current closures"
        return set2node(st) in self.nodes

    def __str__(self):
        s = ""
        for e in sorted(self.closeds):
            s += str(e) + "\n"
        return s

    def reviseboost(self,v):
        self.boosthr = v
        while self.freezer:
            if -self.freezer[0][0] > self.boosthr:
                (spp,st) = heappop(self.freezer)
                heappush(self.ready,(self.dataset.nrtr-self.supps[st],st))
            else:
                break


if __name__=="__main__":

    
##    fnm = "lenses_recoded.txt"
##    but cuts testing assumes fnm e13

##    laa = clattice(0.003,"cestas20")

##    exit(1)
    
    fnm = "e13"
##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    
##    la = lattice(0.01,fnm)
##    la = lattice(0.6,fnm)

    la = Lattice(fnm)

    la.boosthr = 0
    for a in la.candClosures():
        print "\nClosures: ", a, la.supps[a]
        print "imm preds:"
        for e in la.immpreds[a]: print e, ",",
        print
        print "all preds:"
        for e in la.allpreds(a): print e, ",",

    exit(2)

    la.boosthr = 1.25
    for e in la.candClosures():
        print e, la.supps[e]
        la.reviseboost(la.boosthr-0.03)

    exit(1)

    print "Closure of ac:", la.close(set2node(auxitset("a c")))
    print "Closure of ab:", la.close(str2node("a b"))
    print "Is ac closed?", la.isclosed(str2node("a c / 7777"))
    print "Is ab closed?", la.isclosed(str2node("a b"))

    
    (y,n) = la._cut(la.close(set2node("a")),int(0.1*statics.scale))
    print "cutting at threshold", 0.1
    print "pos cut at a:", y
    print "neg cut at a:", n

    print "cutting all nodes now at threshold", 0.75
    for nd in la.candClosures():
        print
        print "At:", nd
        print "  mxs:", nd.mxs, "mns:", nd.mns
        (y,n) = la._cut(nd,int(0.75*statics.scale))
        print "pos cut:",
        for st in y: print st,
        print
        print "neg cut:",
        for st in n: print st,
        print


