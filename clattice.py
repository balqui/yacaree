"""
Project: yacaree - copied verbatim from slatt 0.2.2
Package: clattice
Programmers: JLB

#! /usr/bin/python

TO BE REFACTORED FOR YACAREE - add in a first closure miner

slatt info:

Purpose: implement a lattice by lists of antecedents among closed itsets

Offers:
.hist_cuts: all cuts computed so far, so that they are not recomputed
.dump_hist_cuts
.init from dataset, but checks for existence of closure file to see if can spare the apriori call
.computing closure op
.to string method
.scale: to use ints instead of floats for support/confidence bounds
..and also for conf/width/block factor bounds in other classes
..allows one to index already-computed bases or cuts
..and also to handle the choices [0,1]-float versus percent-float transparently

ToDo:
.refactor the handling of omitted nodes in setcuts:
  the conf boost (upper width) bound and the variants of Kr Property 9
  should be treated in the same manner
.raise a more appropriate exception if platform not handled
.check mns and mxs for extreme cases
.handle the call to Borgelt's apriori on Linux
.rethink the scale, now 100000 means three decimal places for percentages
.be able to load only a part of the closures in the available file if desired support is higher than in the file
.review the ticking rates
.if mxs zero, option is conservative estimate minsupp-1
.is it possible to save time somehow using immpreds to compute mxn/mns?
.should become a set of closures? 

yacaree info:

try to make it work as well for slatt
verbosity adapted to use iface, should work
refactor init, try to keep everything else unchanged
except: empty lattice not allowed anymore
compute closures instead of calling apriori and loading them
lists of predecessors, some day must be reduced to Hasse edges
data repeated from Dataset:
scale, univ, nrtr, nrits, nrocc
all these expected not to change along a computation
closures created in order of support, minsupp is the stop criterion

"""

import statics

from verbosity import verbosity
from slanode import slanode, str2node, set2node, auxitset
##from subprocess import call
##from platform import system
from glob import glob
from math import floor
from corr import corr
from heapq import heapify, heappush, heappop
from dataset import Dataset

class clattice:
    """
    Lattice implemented as explicit list of closures with lists of predecessors
    Lists include all the predecessors (transitive closure)
    CLOSFILE checked for existence under name TRANSFILE_clSUPPORTs.txt
    where SUPPORT is the integer indicating existing minimum absolute support
    Fields:
    Scale to avoid floats in supp/conf/etc
    Universe set U
    Number of closures card
    List of closures closeds
    Dictionary of closed predecessors for each closure
    Maximum and minimum supports seen (absolute integers)
    supp_percent, float in [0,100] actually used for the mining
    (may be strictly lower than minsupp actually seen)
    Number of transactions in the original dataset nrtr
    Number of different items in the original dataset nrits
    Number of item occurrences in the original dataset nrocc
    Verbosity v own or received at init
 overriden info:
    Initialization is from Borgelt's apriori v5 output:
      ./apriori.exe -tc -sSUPPORT -u0 -l1 -v" /%a" TRANSFILE.txt CLOSFILE.txt
    Closures expected ordered in the list (option -l1)
    """

    def __init__(self,supp,datasetfilename="",v=None):
        "float supp in [0,1] - read from clos file or create it from dataset"
        if v==None:
            self.v = verbosity()
        else:
            self.v = v
        d = Dataset(datasetfilename)
        self.U = d.univ
        self.scale = statics.scale
        self.closeds = []
        self.card = 0
        self.preds = {} # to refactor into defaultdict
        self.hist_cuts = {}
        self.nrocc = d.nrocc
        self.nrtr = d.nrtr
        self.nrits = d.nrits
        self.supp_percent = self.topercent(supp)
        self.intsupp = floor(supp * self.nrtr) # support bound into absolute int value
        clfilename = "%s_cl%2.3fs.txt" % (datasetfilename,self.supp_percent)
        suchfiles = glob(datasetfilename+"_cl*s.txt")
        if clfilename in suchfiles:
            "avoid computing closures if closures file already available"
            pass
## TO DO: READ AND WRITE CLOSURE FILES - MUST PROGRAM SCRIPT TO FIND
## AN APPROPRIATE CHARACTER TO SEPARATE THE SUPPORT - CONSIDER XML
        if True:
            "this will be the 'else:' when the closure files are handled"
            self.maxsupp = 0
            clos_singl = set([])
            nbord = 0
            self.v.inimessg("Computing closures at support %3.2f%%;" %
                            self.topercent(supp)) 
            self.v.messg("singletons first...") 
            for item in d.univ:
                "initialize (min-)heap with closures of singletons"
                self.v.tick()
                supset = d.occurncs[item]
                supp = len(supset)
                if supp > self.maxsupp: self.maxsupp = supp
                if supp > self.intsupp:
                    clos_singl.add((d.nrtr-supp,
                                    frozenset(d.inters(supset)),
                                    frozenset(supset)))
                else:
                    nbord += 1
            cnt_clos_singl = len(clos_singl)
            self.v.messg(str(cnt_clos_singl) + " such closures; " +
                         "computing larger closures...")
            pend_clos = list(clos_singl.copy())
            heapify(pend_clos)
            self.minsupp = self.nrtr
            while pend_clos:
                "extract largest-support closure and find subsequent ones"
                cl = heappop(pend_clos)
                spp = d.nrtr - cl[0]
                if spp < self.minsupp: self.minsupp = spp
                self.newclosure(cl[1],spp)
                for ext in clos_singl:
                    "try extending with freq closures of singletons"
                    if not ext[1] <= cl[1]:
                        self.v.tick()
                        supportset = cl[2] & ext[2]
                        spp = len(supportset)
                        if spp <= self.intsupp:
                            nbord += 1
                        else:
                            next_clos = frozenset(d.inters(supportset))
                            if next_clos not in [ cc[1] for cc in pend_clos ]:
                                heappush(pend_clos, (d.nrtr-len(supportset),
                                         next_clos, frozenset(supportset)))
        if self.maxsupp < self.nrtr:
            "no bottom itemset, common to all transactions - hence add emtpy"
            self.addempty(self.nrtr)
        else:
            self.v.messg("bottom closure is nonempty;")
        self.v.messg("...done.")
        self.v.messg(str(self.card)+" closures found.") 
        self.v.messg("Additionally checked " + str(nbord) +
                     " infrequent sets as negative border.")
        self.v.inimessg("The max support is "+str(self.maxsupp)+";")
        self.v.messg("the effective absolute support threshold is "+str(self.minsupp)+
                  (", equivalent to %2.3f" % (float(self.minsupp*100)/self.nrtr)) +
                     "% of " + str(self.nrtr) + " transactions.")

    def newclosure(self,st,spp=-1):
        """
        append new node from string st to self.closeds
        CAREFUL, NOW IT IS A SET AND NOT A STRING:
            MUST CHOOSE ACCORDINGLY str2node OR set2node
        if string, support is embedded and spp is -1
            then call to str2node without the spp param
        return new node itself
        initialize its mxs and mns according to nodes already existing
        update mxs and mns values of predecessors and successors
        update the lists of predecessors of its successors
        """
        node = set2node(st,spp)
        node.mxs = 0
        node.mns = self.nrtr
        above = []
        below = []
        for e in self.closeds:
            "list existing nodes above and below, break if a duplicate is found"
            if node < e:
                "a superset found"
                above.append(e)
                if e.supp > node.mxs: node.mxs = e.supp
            elif e < node:
                "a subset found"
                below.append(e)
                if e.supp < node.mns: 
                    node.mns = e.supp
            elif e == node:
                "repeated closure! don't return node, causes error in init"
                self.v.errmessg("Itemset from "+str(st)+" duplicated.")
                break
        else:
            "not found, correct nonduplicate node: add to closeds and to preds lists above"
            self.closeds.append(node)
            self.U.update(node)
            self.card += 1
            self.preds[node] = []
            if len(above)>0:
                "closures in file not in order - should never happen"
                self.v.errmessg("Closure "+st+" is a predecessor of earlier nodes")
####                self.mustsort = True
####                if len(above)==1:
####                    self.v.messg("("+str(above[0])+")\n")
####            for e in above:
####                self.preds[e].append(node)
####                if e.mns > node.supp: e.mns = node.supp
            for e in below:
                self.preds[node].append(e)
                if node.supp > e.mxs: e.mxs = node.supp
            return node

    def addempty(self,nrtr):
        """
        add emptyset as closure, with nrtr as support
        (pushed into the front, not appended)
        mns for emptyset nrtr for today, somewhat unclear
        (kills down to 1 the width of empty-antecedent rules, maybe rightly so)
        """
        node = str2node()
        node.setsupp(nrtr)
        self.preds[node] = []
        node.mns = nrtr
        node.mxs = 0
        for e in self.closeds:
            self.preds[e].append(node)
            if e.mns > node.supp: e.mns = node.supp
            if e.supp > node.mxs: node.mxs= e.supp
        self.card += 1
        self.closeds.insert(0,node)

    def topercent(self,anysupp):
        """
        anysupp expected in [0,1], eg a support bound
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places)
        """
        return 100.0*floor(self.scale*anysupp)/self.scale

    def __str__(self):
        s = ""
        for e in sorted(self.closeds):
            s += str(e) + "\n"
        return s

    def close(self,st):
        "closure of set st according to current closures list - slow for now"
        over = [ e for e in self.closeds if st <= e ]
        if len(over)>0:
            e = over[0]
        else:
            "CAREFUL: what if st is not included in self.U?"
            e = set2node(self.U)
        for e1 in over:
            if e1 < e:
                e = e1
        return e

    def isclosed(self,st):
        "test closedness of set st according to current closures list"
        return st in self.closeds

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
##    fnm = "lenses_recoded.txt"
##    but cuts testing assumes fnm e13

    laa = clattice(0.003,"cestas20")

    exit(1)
    
    fnm = "e13.txt"
    la = clattice(0,fnm)
    la.v.inimessg("Module clattice running as test on file "+fnm)
    la.v.inimessg("Lattice read in:\n")
    la.v.messg(str(la))

    print "Closure of ac:", la.close(set2node(auxitset("a c")))
    print "Closure of ab:", la.close(str2node("a b"))
    print "Is ac closed?", la.isclosed(str2node("a c / 7777"))
    print "Is ab closed?", la.isclosed(str2node("a b"))

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


##        self.mustsort = False
##        self.v.inimessg("Initializing lattice") 
##        if datasetfilename == "":
##            self.v.messg(" with just a bottom empty closure.")
##            self.supp_percent = 0.0
##            self.card = 0
##            self.maxsupp = 0
##            self.minsupp = 0
##            self.preds = {}
##            self.addempty(0)
##        else:
###          try:
##            "MUST MOVE OFF HERE THE PARAMETER COMPUTATION"
##            datasetfile = file("%s" % datasetfilename)
##            self.v.zero(2500)
##            self.v.messg("from file "+datasetfilename+"... computing parameters...")
##            self.nrocc = 0
##            self.nrtr = 0
##            uset = set([])
##            for line in datasetfile:
##                self.v.tick()
##                self.nrtr += 1
##                for el in line.strip().split():
##                    if len(el)>0:
##                        self.nrocc += 1
##                        uset.add(el)
##            self.nrits = len(uset)
##            if supp == 0:
##                "apriori implementation might not work with support zero"
##                self.supp_percent = 0.001
##            else:
##                "there remains a scale issue to look at in the clfile name"

##            # use / to separate itemset from support - check slanode is consistent
##            cmmnd = ('./apriori.exe -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % (self.supp_percent,datasetfilename)) + clfilename
##            pass
##            elif system()=="Darwin":
##                cmmnd = ('./aprioriD -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % (self.supp_percent,datasetfilename)) + clfilename
##                call(cmmnd,shell=True)
##            elif system()=="Linux":
##                "ToDo: make this case work"
####                cmmnd = ('./aprioriL32 -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % (self.supp_percent,datasetfilename)) + clfilename
####                call(cmmnd,shell=True)
##                self.v.errmessg("Platform "+system()+" not handled yet, sorry")
##            elif system()=="Windows" or system()=="Microsoft":
##                self.v.messg("platform appears to be "+system()+";")
##                self.v.messg("computing closures by: \n        "+cmmnd+"\n")
##                call(cmmnd)
##            elif system()=="CYGWIN_NT-5.1":
##                self.v.messg("platform appears to be "+system()+";")
##                self.v.messg("computing closures by: \n        "+cmmnd+"\n")
##                call(cmmnd,shell=True)
##            else:
##                "unhandled platform - hack: artificially raise exception"
##                self.v.errmessg("Platform "+system()+" not handled yet, sorry")
##                ff = file("NonexistentFileToRaiseAnExceptionDueToUnhandledSystem")

##            self.card = 0
##            self.maxsupp = 0
##            self.minsupp = self.nrtr+1
##            self.preds = {}
##            self.v.zero(250)
##            self.v.messg("...loading closures in...")
##            for line in file(clfilename):
##                "ToDo: maybe the file has lower support than desired and we do not want all closures there"
##                self.v.tick()
##                newnode = self.newclosure(line)
##                if newnode.supp > self.maxsupp:
##                    self.maxsupp = newnode.supp
##                if newnode.supp != 0 and newnode.supp < self.minsupp:
##                    self.minsupp = newnode.supp
##            self.v.messg("...done;")

##            if self.mustsort:
##                self.v.messg("sorting...")
##                self.closeds.sort()
##                self.mustsort = False

###          except:
###            "ToDo: program a decent exception"
###            self.v.errmessg("Please check file " + datasetfilename + " is there, platform is handled, and everything else.")

