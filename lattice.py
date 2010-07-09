"""
Package: lattice based on slatt - but keep only Hasse edges,
that is, list of immediate predecessors for each node



Programmers: JLB

Purpose: implement a lattice by lists of antecedents among closed itsets

Offers:
.init from clminer
.cuts at a given conf, and restricted to certain closures
.hist_cuts: all cuts computed so far, so that they are not recomputed
.dump_hist_cuts
.computing closure op
.to string method

ToDo:

.read it in from XML file, edges included
.recover the handling of mns/mxs and check their use in extreme cases
.if mxs zero, option is conservative estimate minsupp-1
.is it possible to save time somehow using immpreds to compute mxn/mns?
.rethink the scale, now 100000 means three decimal places for percentages
.be able to load only a part of the closures in the available file if desired support is higher than in the file
.review the ticking rates
.should become a set of closures? 
"""

from iface import iface
from dataset import Dataset
from clminer import ClMiner
from border import Border
from corr import corr
from collections import defaultdict

class lattice:
    """
    Lattice implemented as explicit list of closures from clminer
    with a dict of closed immediate predecessors for each closure
    from border
    ToDo: make it become a mere iterator (how to handle the filtering then?)
    Closures expected ordered in the list by decreasing supports or increasing sizes
    """

    def __init__(self,supp,datasetfilename):
        "float supp in [0,1]"
        self.dataset = Dataset(datasetfilename)
        miner = ClMiner(supp,self.dataset)
        bord = Border()
        self.hist_cuts = {}
        self.closeds = []
        self.nodes = defaultdict(list)
        for node in miner.mineclosures():
            """
            set up preds and everything -
            closures come in either nonincreasing support or nondecreasing size
            hence all subsets of each closure come before it - needed for the inters (correct?)
            if dict could be iterated in order of arrival, can dispose of closeds and use nodes instead
            """
            self.closeds.append(node)
            self.nodes[node] = bord.cover_update(node,self)
            bord.append(node)

    def allpreds(self,node):
        "iterator for all predecessors, dfs, needs to avoid dups"
        pending = [ e for e in self.nodes[node] ]
        handled = set(pending)
        while pending:
            p = pending.pop()
            yield p
            for q in self.nodes[p]:
                if q not in handled:
                    handled.add(q)
                    pending.append(q)


    def __str__(self):
        s = ""
        for e in sorted(self.closeds):
            s += str(e) + "\n"
        return s

    def close(self,st):
        "closure of set st according to current closures list"
## A GOOD IDEA TO ACCELERATE BUT SOMETIMES RETURNS SUPP-LESS NODES
##        fst = set2node(st)
##        if fst in self.nodes:
##            "fast to test with hash, little expense may save a lot"
##            return fst
        for node in self.closeds:
            "use nodes instead when possible - risks being slow"
            if st <= node:
                "largest support closure containing st"
                break
        else:
            "should check that node is included in universe"
            node = set2node(self.U)
        return node

    def isclosed(self,st):
        "test closedness of set st according to current closures"
        return set2node(st) in self.nodes

    def dump_hist_cuts(self):
        "prints out all the cuts so far - useful mostly for testing"
        for e in self.hist_cuts.keys():
            print "\nMinimal closed antecedents at conf thr", e
            pos = self.hist_cuts[e][0]
            for ee in pos.keys():
                print ee, ":",
                for eee in pos[ee]: print eee,
                print
            print "Maximal closed nonantecedents at conf thr", e
            neg = self.hist_cuts[e][1]
            for ee in neg.keys():
                print ee, ":",
                for eee in neg[ee]: print eee,
                print

    def setcuts(self,scsthr,sccthr,forget=False,skip=None,skippar=0):
        """
        supp/conf already scaled thrs in [0,self.scale]
        computes all cuts for that supp/conf thresholds, if not computed yet;
        keeps them in hist_cuts to avoid duplicate computation (unless forget);
        the cut for each node consists of two corrs, pos and neg border:
        hist_cuts : supp/conf thr -> (pos,neg)
        pos : node -> min ants,  neg : node -> max nonants
        wish to be able to use it for a support different from self.minsupp
        (unclear whether it works now in that case)
        Things that probably do not work now:
        Bstar may require a support improvement wrt larger closures
        signaled by skip not None AND skippar (improv) not zero
        Kr/BC heuristics may require a conf-based check on nodes,
        signaled by skip not None and skippar (conf) not zero
        """
        if (scsthr,sccthr) in self.hist_cuts.keys():
            "use cached version if it is there"
            return self.hist_cuts[scsthr,sccthr]
        if skip is not None and skippar != 0:
            "risk of not all closures traversed, don't cache the result"
            forget = True
        else:
            "skip is None or skippar is zero, then no skipping"
            skip = never
        cpos = corr()
        cneg = corr()
        self.v.zero(500)
        self.v.messg("...computing (non-)antecedents...")
        for nod in self.closeds:
            "review carefully and document this loop"
            if skip(nod,skippar,self.scale):
                "we will not compute rules from this closure"
                continue
            self.v.tick()
            if self.scale*nod.supp >= self.nrtr*scsthr:
                pos, neg = self._cut(nod,sccthr) 
                cpos[nod] = pos
                cneg[nod] = neg
        if not forget: self.hist_cuts[scsthr,sccthr] = cpos, cneg
        self.v.messg("...done;")
        return cpos, cneg

    def _cut(self,node,thr):
        """
        splits preds of node at cut given by
        min thr-antecedents and max non-thr-antecedents
        think about alternative algorithmics
        thr expected scaled according to self.scale
        """
        yesants = []
        notants = []
        for m in self.preds[node]:
            "there must be a better way of doing all this!"
            if self.scale*node.supp >= thr*m.supp:
                yesants.append(m)
            else:
                notants.append(m)
        minants = []
        for m in yesants:
            "keep only minimal antecedents - candidate to separate program?"
            for mm in yesants:
                if mm < m:
                    break
            else:
                minants.append(m)
        maxnonants = []
        for m in notants:
            "keep only maximal nonantecedents"
            for mm in notants:
                if m < mm:
                    break
            else:
                maxnonants.append(m)
        return (minants,maxnonants)

def never(n,s,t):
    return False

if __name__=="__main__":


    from slanode import set2node, auxitset, str2node
    
##    fnm = "lenses_recoded.txt"
##    but cuts testing assumes fnm e13

##    laa = clattice(0.003,"cestas20")

##    exit(1)
    
    fnm = "e13"
##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    
    la = lattice(0.01,fnm)

    for a in sorted(la.nodes):
        print a,
        print "imm preds:"
        for e in la.nodes[a]: print e, ",",
        print
        print "all preds:"
        for e in la.allpreds(a): print e, ",",
        print

    exit(1)        

    print "Closure of ac:", la.close(set2node(auxitset("a c")))
    print "Closure of ab:", la.close(str2node("a b"))
    print "Is ac closed?", la.isclosed(str2node("a c / 7777"))
    print "Is ab closed?", la.isclosed(str2node("a b"))

    exit(4)
    
    (y,n) = la._cut(la.close(set2node("a")),int(0.1*la.scale))
    print "cutting at threshold", 0.1
    print "pos cut at a:", y
    print "neg cut at a:", n

    print "cutting all nodes now at threshold", 0.75
    for nd in la.closeds:
        print
        print "At:", nd
        print "  mxs:", nd.mxs, "mns:", nd.mns
        (y,n) = la._cut(nd,int(0.75*la.scale))
        print "pos cut:",
        for st in y: print st,
        print
        print "neg cut:",
        for st in n: print st,
        print


