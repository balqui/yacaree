"""
yacaree

Current revision: mid Pluviose 2025

Programmers: JLB

Previous version docstring:
Relies on implminer and partialruleminer for the actual mining.
Each of these needs its own different checkrule (with or without closures).
Here we keep the Lattice and the tracking of the boost threshold.
Also we call from here the main iterator in Lattice and run
each of implminer and partialruleminer on each closure.
Plan is to change this into two (or more?) separate processes (tricky).
"""


from iface import IFace
from lattice import Lattice
from rule import Rule
from itset import ItSet
from math import isfinite
from heapq import heappush
from iter_subsets import all_proper_subsets

##from heapq import heapify, heappush, heappop
##from collections import defaultdict

# ~ from implminer import mine_implications

# ~ from partialruleminer import mine_partial_rules

class ImplMiner:

    def __init__(self):
        try:
            from hytra import HyperGraph, transv_zero
        except ImportError:
            IFace.old_hygr = True
            from hypergraph_old import transv_zero, \
                                       hypergraph as HyperGraph
        self.hypergraph = HyperGraph
        self.transv = transv_zero
    
    def _faces(self, itst, listpred):
        "listpred immediate preds of itst, hypergraph of differences"
        return self.hypergraph(itst, 
                             [ itst.difference(e) for e in listpred ])

# ~ took out the very ugly old_hygr global

    def set_m_impr(self, rul, miner):
        "rul assumed to be an implication, test std (non-closure) mult impr"
        if rul.conf < 1:
            IFace.reporterror("Multiplicative improvement test expected" +
                " an implication but got instead " + str(rul))
        if rul.cn.suppratio < IFace.hpar.abssuppratio:
            "CAVEAT: Plan to push the suppratio constraint into the cl mining"
            # ~ print(" .. no, low suppratio", rul.cn.suppratio)
            return False
        altconf = 0
        cl_ants = set([])
        for an2 in all_proper_subsets(set(rul.an)):
            an2cl = miner.close(an2)
            if an2cl in cl_ants:
                "CAVEAT, TEST TO BE REMOVED SOON"
                print(" .. repeated", an2cl, "closure of", an2, "for", rul)
            else:
                cl_ants.add(an2cl)
            cn2 = miner.close(rul.rcn.union(an2))
            if cn2.supp * IFace.hpar.absoluteboost > an2cl.supp:
                # ~ print(" .. discarding", rul, an2, cn2, cn2.supp / an2cl.supp)
                return False
            if cn2.supp > altconf * an2cl.supp:
                altconf = cn2.supp / an2cl.supp
        if altconf > 0:
            rul.m_impr = 1/altconf
        else:
            "CAVEAT: Acceptable for empty antecedents, think."
            IFace.reportwarning("Null altconf for Rule " + str(rul))
            rul.m_impr = rul.cn.suppratio # will not disturb
        rul.set_cboo()
        return True


    def mine_implications(self, latt, cn):
        """
        Gets a closure cn, with suppratio if known: find implications
        with it as consequent.
        If all supersets below minsupp, suppratio not known.
        CAVEAT: keep count somehow of discarded implications!
        """
        mingens = list( m 
            for m in self.transv(self._faces(cn, latt[cn])).hyedges )
        # ~ print(" == mingens of", cn, ":", mingens)
        if not mingens:
            "The error reporting will exit the program."
            IFace.reporterror("No minimum generators for " + 
                f"{str(cn)}, predecessors: [ " +
                f"{'; '.join(str(e) for e in latt[cn])} ]")
        if len(cn) > len(mingens[0]):
            "o/w cn is a free set, its own unique mingen, no rules"
            for an in mingens:
                # ~ print(" == making a rule out of", an, "and", latt[cn])
                an = frozenset(an)
                if an in latt:
                    "CAVEAT: look it up on clminer instead?"
                    IFace.reporterror(str(an) + 
                        " in lattice but should not be," + 
                        " something seems wrong.")
                else: 
                    rul = Rule(an, cn, full_impl = True)
                    if self.set_m_impr(rul, latt.miner):
                        yield rul







class RuleMiner: # Does not subclass Lattice anymore

    def __init__(self, hpar, dataset, supprat = True):
        "some codes, reserved rules, and average lift so far"
        self.latt = Lattice(dataset)
        if not supprat:
            self.latt.boosthr = 1 # SHORTCIRCUIT SUPPRATIO CONSTRAINT PUSH
        self.count = 0
        self.im = ImplMiner()

    def minerules(self, supp = -1):
        """
        supp == -1: use hpar.genabsupp;
        o/w, expected in [0, 1]: use it instead.
        Early version had an undocumented 'safetysupp' instead.
        """
        for cn in self.latt.candidate_closures(supp): 
            if cn:
                for rul in self.im.mine_implications(self.latt, cn):
                    self.count += 1
                    yield rul
                # ~ for rul in mine_partial_rules(self, cn):
                    # ~ if rul.conf > IFace.hpar.confthr:
                        # ~ self.count += 1
                        # ~ yield rul


if __name__=="__main__":

    from hyperparam import HyperParam
    from filenames import FileNames
    from dataset import Dataset

##    fnm = "pumsb_star"
##    fnm = "cmc-full"
##    fnm = "adultrain"
    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/toy_rr"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    # ~ fnm = "../data/e5b"
    # ~ fnm = "../data/e5"
    # ~ fnm = "../data/p5.td"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"
    # ~ fnm = "../data/votesTr" 
    # ~ fnm = "../data/NOW" 
    fnm = "../data/papersTr" # FILLS 15GB MEMORY ANYHOW EVEN WITH THE TOTAL SUPPORT SET LENGTHS LIMIT
    # The next work thanks to the limit on the total support set lengths
    # ~ fnm = "../data/chess.td"   # Fills 8GB memory with small heap size
    # ~ fnm = "../data/connect.td" # Fills 8GB memory with ridiculous heap
                                   # size and less than 5000 closures

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()
    # ~ supp = 0.01

    miner = RuleMiner(IFace.hpar, d)
    rulist = list()
    for rul in miner.minerules(): # supp):
        rulist.append(rul)
        # ~ IFace.report(str(miner.count) + "/ " + str(rul))
    if input(f"Show {len(rulist)} implications? "):
        for cnt, rul in enumerate(sorted(rulist, 
              key = lambda r: r.cboo, reverse = True)):
            print(cnt + 1, "/", rul, rul.cn.suppratio, rul.m_impr)


