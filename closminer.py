"""
Project: slatt
Package: closminer
Programmers: JLB

Purpuse: obtain list of closures for building a clattice

Several ways:
1/ find them precomputed in a Borgelt apriori output file (deprecated)
2/ find them precomputed in an XML file
3/ mine them by calling external binary for Borgelt's apriori v5.4
4/ mine them by local internal algorithm

If xmlinput is set to True, and the xml file is found, will try 2,
otherwise the next consideration applies

If use_external_miner is set to True, will try 1, then 3 (eg if no
closures file found), then 4 (eg if external apriori not found)

Otherwise 4 is attempted directly

Default is xmlinput False, use_external_miner True

Borgelt's apriori call uses '/' to separate itemset from support,
 will break down if that char appears in any of the items;
 this can be changed below but must change slanode accordingly

Method xmlize() available to write the closures to the XML file

keeps dataset info (scale, nrtr and such) and 
 materialized list of closures
 
nonmaterialized iterator and badly needed 
 refactoring left to a brother project for the time being

ToDo:
 set up a local database of filenames and supports
 handle the call to Borgelt's apriori on Linux

"""

import xml.etree.ElementTree
import xml.dom.minidom

from collections import defaultdict
from verbosity import verbosity
from subprocess import call
from platform import system
from heapq import heapify, heappush, heappop
from slanode import slanode, str2node, set2node, auxitset
from glob import glob
from math import floor


class closminer:

    def __init__(self,supp,datasetfilename,v=None,xmlinput=False,externalminer=True):
        """
        support float in [0,1], see above for rest of parameters
        """
        self.use_external_miner = externalminer
        self.read_from_XML_file = xmlinput
        if v==None:
            self.v = verbosity()
        else:
            self.v = v
        self.U = set([])
        self.scale = 100000
        self.datasetfilename = datasetfilename
        self.supp_percent = self.topercent(supp)
        self.xmlfilename = "%s_cl%2.3fs.xml" % (datasetfilename,self.supp_percent)
        self.closeds = []
        self.card = 0
        self.mustsort = False
        self.v.inimessg("Initializing lattice") 
        if datasetfilename == "":
            self.v.messg(" with just a bottom empty closure.")
            self.nrocc = 0
            self.nrtr = 0
            self.nrits = 0
            self.supp_percent = 0.0
            self.card = 0
            self.maxsupp = 0
            self.minsupp = 0
            self.addempty(0)
        else:
            try:
                datasetfile = open(datasetfilename+".txt")
            except IOError:
                self.v.errmessg("Could not open file "+datasetfilename+".txt")
                exit(0)
            self.v.zero(2500)
            self.v.messg("from file "+datasetfilename+"... computing parameters...")
            self.nrocc = 0
            self.nrtr = 0
            self.U = set([])
            self.transcns = defaultdict(set)
            self.occurncs = defaultdict(set)
            for line in datasetfile:
                self.v.tick()
                for el in line.strip().split():
                    if len(el)>0:
                        isempty = False
                        self.nrocc += 1
                        self.U.add(el)
                        self.transcns[self.nrtr].add(el)
                        self.occurncs[el].add(self.nrtr)
                if not isempty:
                    self.nrtr += 1
            self.nrits = len(self.U)
            self.intsupp = floor(supp * self.nrtr) # support bound into absolute int value
            if supp == 0:
                "Borgelt's apriori might not work with support zero"
                self.supp_percent = 0.001
            else:
                "there remains a scale issue to look at in the clfile name"
                self.supp_percent = self.topercent(supp)
            if self.read_from_XML_file:
                self.v.messg("...reading closures from XML file...")
                try:
                    self.dexmlize(self.xmlfilename)
                    self.v.messg(str(self.card)+" closures found.") 
                    return
                except IOError:
                    self.v.errmessg(self.xmlfilename+" not found, falling back to mining process.")
            nbord = 0
            if self.use_external_miner:
                "try using results of external apriori, or calling it"
                clfilename = "%s_cl%2.3fs.txt" % (datasetfilename,self.supp_percent)
                suchfiles = glob(datasetfilename+"_cl*s.txt")
                cmmnd = ('./apriori.exe -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % 
                         (self.supp_percent,datasetfilename+".txt")) + clfilename
                if clfilename in suchfiles:
                    "avoid calling apriori if closures file already available"
                    self.v.messg("...reading closures from file "+clfilename+"...")
                elif system()=="Darwin":
                    if not glob("aprioriD"):
                        self.use_external_miner = False
                        self.v.errmessg("aprioriD not found, falling back on internal closure miner")
                    else:
                        cmmnd = ('./aprioriD -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % 
                                 (self.supp_percent,datasetfilename+".txt")) + clfilename
                        call(cmmnd,shell=True)
                elif system()=="Linux":
                    "ToDo: make this case work"
##                cmmnd = ('./aprioriL32 -tc -l1 -u0 -v" /%%a" -s%2.3f %s ' % 
##                         (self.supp_percent,datasetfilename)) + clfilename
##                call(cmmnd,shell=True)
                    self.v.errmessg("Platform "+system()+" not handled yet, sorry")
                    self.use_external_miner = False
                elif system()=="Windows" or system()=="Microsoft":
                    self.v.messg("platform appears to be "+system()+";")
                    self.v.messg("computing closures by: \n        "+cmmnd+"\n")
                    if not glob("apriori.exe"):
                        self.use_external_miner = False
                        self.v.errmessg("apriori.exe not found, falling back on internal closure miner")
                    else:
                        call(cmmnd)
                elif system()=="CYGWIN_NT-5.1":
                    self.v.messg("platform appears to be "+system()+";")
                    self.v.messg("computing closures by: \n        "+cmmnd+"\n")
                    if not glob("apriori.exe"):
                        self.use_external_miner = False
                        self.v.errmessg("apriori.exe not found, falling back on internal closure miner")
                    else:
                        call(cmmnd,shell=True)
                elif system()=="CYGWIN_NT-6.1-WOW64":
                    self.v.messg("platform appears to be "+system()+";")
                    self.v.messg("computing closures by: \n        "+cmmnd+"\n")
                    call(cmmnd,shell=True)
                else:
                    "unhandled platform"
                    self.v.errmessg("Platform "+system()+" not handled yet, sorry")
                    self.use_external_miner = False
                if self.use_external_miner:
                    "closures file in place, either was there or just computed"
                    self.card = 0
                    self.maxsupp = 0
                    self.minsupp = self.nrtr+1
                    self.v.zero(250)
                    self.v.messg("...loading closures in...")
                    for line in file(clfilename):
                        """
                        ToDo: maybe the file has lower support 
                        than desired and we do not want all closures there
                        """
                        self.v.tick()
                        node = str2node(line)
                        self.closeds.append(node)
                        self.card += 1
                        if node.supp > self.maxsupp:
                            self.maxsupp = node.supp
                        if node.supp != 0 and node.supp < self.minsupp:
                            self.minsupp = node.supp
            if not self.use_external_miner:
                """
                use internal miner either as asked or 
                because could not use external apriori
                """
                self.maxsupp = 0
                clos_singl = set([])
                self.v.inimessg("Computing closures at support %3.2f%%;" %
                                self.topercent(supp)) 
                self.v.messg("singletons first...") 
                for item in self.U:
                    "initialize (min-)heap with closures of singletons"
                    self.v.tick()
                    supset = self.occurncs[item]
                    supp = len(supset)
                    if supp > self.maxsupp: self.maxsupp = supp
                    if supp > self.intsupp:
                        clos_singl.add((self.nrtr-supp, 
                                        frozenset(self.inters(supset)),
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
                    spp = self.nrtr - cl[0]
                    if spp < self.minsupp:
                        self.minsupp = spp
                    node = set2node(cl[1],spp)
                    self.closeds.append(node)
                    self.U.update(node)
                    self.card += 1
                    for ext in clos_singl:
                        "try extending with freq closures of singletons"
                        if not ext[1] <= cl[1]:
                            self.v.tick()
                            supportset = cl[2] & ext[2]
                            spp = len(supportset)
                            if spp <= self.intsupp:
                                nbord += 1
                            else:
                                next_clos = frozenset(self.inters(supportset))
                                if next_clos not in [ cc[1] for cc in pend_clos ]:
                                    heappush(pend_clos, (self.nrtr-len(supportset),
                                                         next_clos, frozenset(supportset)))

        if self.maxsupp < self.nrtr:
            "no bottom itemset, common to all transactions - hence add emtpy"
            self.addempty(self.nrtr)
        else:
            self.v.messg("bottom closure is nonempty;")
        self.v.messg("...done.")

        if self.mustsort:
            self.v.messg("sorting...")
            self.closeds.sort()
            self.mustsort = False

        self.v.messg(str(self.card)+" closures found.") 
        if nbord != 0:
            "This info only available if the local miner was used"
            self.v.messg("Additionally checked " + str(nbord) +
                         " infrequent sets as negative border.")
        self.v.inimessg("The max support is "+str(self.maxsupp)+";")
        self.v.messg("the effective absolute support threshold is "+str(self.minsupp)+
                  (", equivalent to %2.3f" % (float(self.minsupp*100)/self.nrtr)) +
                     "% of " + str(self.nrtr) + " transactions.")

    def topercent(self,anysupp):
        """
        anysupp expected in [0,1], eg a support bound
        gets translated into percent and truncated according to scale
        (e.g. for scale 100000 means three decimal places)
        """
        return 100.0*floor(self.scale*anysupp)/self.scale

    def addempty(self,nrtr):
        """
        add emptyset as closure, with nrtr as support
        (pushed into the front, not appended)
        """
        node = str2node()
        node.setsupp(nrtr)
        self.card += 1
        self.closeds.insert(0,node)

    def xmlize(self,outfnm=""):
        "TO DO: move to use the ElementTree API instead of minidom"
        xmldoc = xml.dom.minidom.Document()
        topelem = xmldoc.createElement("xmlclosurespace")
        xmldoc.appendChild(topelem)
        contextelem = xmldoc.createElement("context")
        closelem = xmldoc.createElement("closures")
        topelem.appendChild(contextelem)
        topelem.appendChild(closelem)
        paramelem = xmldoc.createElement("parameters")
        paramelem.setAttribute("filename",self.datasetfilename)
        paramelem.setAttribute("support",str(self.supp_percent)+"%")
        contextelem.appendChild(paramelem)

        cd = defaultdict(list)
        for c in self.closeds:
            cd[c.supp].append(c)
    
        for s in reversed(sorted(cd)):
            cls = sorted([(len(c),hash(c),c) for c in cd[s]])
            for c in cls:
                clelem = xmldoc.createElement("closure")
                clelem.setAttribute("support",str(c[2].supp))
                clelem.setAttribute("card",str(c[0]))
                clelem.setAttribute("hashcode",str(c[1]))
                for it in sorted(c[2]):
                    itemelem = xmldoc.createElement("item")
                    itemelem.setAttribute("value",str(it))
                    clelem.appendChild(itemelem)
                closelem.appendChild(clelem)
        if outfnm:
            f = open(outfnm,"w")
        else:
            f = open(self.xmlfilename,"w")
        f.write(xmldoc.toprettyxml())
        f.close()

    def dexmlize(self,clfilename=""):
        """
        closeds already is []
        ToDo: check support in xml file,
        read/write further params there
        (e.g. dataset params)...
        """
        if not clfilename:
            clfilename = self.xmlfilename
        xmldoc = xml.etree.ElementTree.parse(clfilename)
        elemclos = xmldoc.find("closures")
        for clo in elemclos.getchildren():
            "handle a closed set"
            s = set()
            for itelem in clo.getchildren():
                "to do: check they are items"
                it = itelem.get("value")
                s.add(it)
            clos = set2node(s,int(clo.get("support")))
            self.closeds.append(clos)
            self.card += 1

    def inters(self,lstr):
        "for an iterable of transactions lstr, return their intersection"
        items = self.U.copy()
        for t in lstr:
            items &= self.transcns[t]
        return items
            

if __name__=="__main__":

    dsfnm = "e13"
    supp = 0.001
##    dsfnm = "pumsb_star"
##    supp = 0.7
##    dsfnm = "lenses_recoded"
##    supp = 0.1


    c = closminer(supp,dsfnm,xmlinput=True)

    print c.closeds

    c.xmlize()
    