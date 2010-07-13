"""
Project: yacaree - based on evolutions of slatt's clattice
Programmers: JLB

Iterator that provides, one by one, in order of 
 decreasing support, all the closures
 for a given dataset and support bound

check heapdict - min heapq from std lib requires sign change of supp

data in Dataset: univ, nrtr, nrits, nrocc

ToDo:

xml must migrate from here to lattice and keep the Hasse edges (optionally maybe)

xml filename should include in the name not the supp but the maxnonsupp

get it from neg border and then glob files and pick the one with highest
maxnonsupp that is below supp, if it exists, o/w must mine

load only a part of the closures in the available file, if desired support
is higher than in the file

"""

import xml.etree.ElementTree
import statics

from itset import ItSet

from math import floor
from iface import iface
from dataset import Dataset
##from slanode import slanode, str2node, set2node, auxitset
from heapq import heapify, heappush, heappop
##from glob import glob

class ClMiner:
    """

    """

    def __init__(self,supp,dataset):
        "float supp in [0,1] - read from clos file or create it from dataset"
        self.supp = supp
        self.dataset = dataset
        self.supp_percent = self.topercent(supp)
        self.xmlfilename = "%s_cl%2.3fs.xml" % (dataset.filename,self.supp_percent)
        self.card = 0
        self.negbordsize = 0
        self.maxnonsupp = 0
        self.maxitemsupp = 0
        self.minsupp = 0
        self.intsupp = floor(supp * dataset.nrtr) # support bound into absolute int value
        try:
            clfile = open(self.xmlfilename)
            self.mineclosures = self.readclosures
        except IOError:
            "xml stored closures not found, must run miner"
            self.mineclosures = self.computeclosures

    def computeclosures(self):
        "no closures file, iterator must mine closed sets"
        clos_singl = set([])
        self.negbordsize = 0
        iface.report("Computing closures at support %3.2f%%;" %
                        self.topercent(self.supp)) 
        iface.say("initializing singletons...") # reserve to only very verbose
        self.maxitemsupp = 0
        self.maxnonsupp = 0
        for item in self.dataset.univ:
            "initialize (min-)heap with closures of singletons"
            iface.pong() # reserve to only verbose
            supset = self.dataset.occurncs[item]
            supp = len(supset)
            if supp > self.maxitemsupp: self.maxitemsupp = supp
            if supp > self.intsupp:
                "probably very slow"
                clos_singl.add((self.dataset.nrtr-supp,
                                frozenset(self.dataset.inters(supset)),
                                frozenset(supset)))
            else:
                self.negbordsize += 1
                if supp > self.maxnonsupp:
                    self.maxnonsupp = supp
        cnt_clos_singl = len(clos_singl)
        iface.say(str(cnt_clos_singl) + " singleton-based closures.\n") # reserve to only very verbose
        if self.maxitemsupp < self.dataset.nrtr:
            "largest support on empty closure"
            yield (ItSet([]),self.dataset.nrtr)
            self.card += 1
        pend_clos = list(clos_singl.copy())
        heapify(pend_clos)
        self.minsupp = self.dataset.nrtr
        while pend_clos:
            "extract largest-support closure and find subsequent ones"
            cl = heappop(pend_clos)
            spp = self.dataset.nrtr - cl[0]
            self.card += 1
            yield (ItSet(cl[1]),spp)
            for ext in clos_singl:
                "try extending with freq closures of singletons"
                if not ext[1] <= cl[1]:
                    "no further pongs, take care of this upon using iterator"
                    supportset = cl[2] & ext[2]
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        self.negbordsize += 1
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        if spp < self.minsupp:
                            self.minsupp = spp
                        next_clos = frozenset(self.dataset.inters(supportset))
                        if next_clos not in [ cc[1] for cc in pend_clos ]:
                            heappush(pend_clos, (self.dataset.nrtr-len(supportset),
                                     next_clos, frozenset(supportset)))
##        iface.endreport()

    def readclosures(self):
        """
        ToDo: check support in xml file,
        read/write further params there
        (e.g. dataset params, negbordsize, max (non)supp, min supp abs/%)
        """
        iface.report("Loading closures from XML file %s;" %
                     self.xmlfilename) 
        xmldoc = xml.etree.ElementTree.parse(self.xmlfilename)
        elemclos = xmldoc.find("closures")
        for clo in elemclos.getchildren():
            "handle a closed set"
            iface.pong()
            s = set()
            for itelem in clo.getchildren():
                "to do: check they are items"
                it = itelem.get("value")
                s.add(it)
            clos = (ItSet(s),int(clo.get("support")))
            self.card += 1
            yield clos
        iface.endreport()

    def topercent(self,anysupp):
        """
        anysupp expected in [0,1], eg a support bound
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places)
        """
        return 100.0*floor(statics.scale*anysupp)/statics.scale

if __name__=="__main__":

    support = 0.15    
##    support = 0.5
##    fnm = "lenses_recoded"
    fnm = "e13"
##    fnm = "exbordalg"
##    fnm = "pumsb_star"
    iface.report("Module clminer running as test on file " +
                 fnm + ".txt with support " + ("%2.3f%%" % support))
    miner = ClMiner(support,Dataset(fnm+".txt"))
    iface.report(str(miner.card)+" closures found.") 
    iface.say("Additionally checked " + str(miner.negbordsize) +
              " infrequent sets as negative border.")
    iface.say("The max support is "+str(miner.maxitemsupp)+".")
    iface.say("The max nonsupport is "+str(miner.maxnonsupp)+".")
    iface.say("The effective absolute support threshold is "+str(miner.minsupp)+
                  (", equivalent to %2.3f" % (float(miner.minsupp*100)/miner.dataset.nrtr)) +
                   "% of " + str(miner.dataset.nrtr) + " transactions.")

    iface.endreport()

    for e in miner.mineclosures():
        iface.say(str(e[0])+" ("+str(e[1])+")\n")
