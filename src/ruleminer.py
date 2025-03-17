"""
yacaree

Current revision: late Pluviose 2025

Programmers: JLB

Calls the main iterator in Lattice and runs each of 
an ImplMiner and a PartRulMiner on each closure.
Plan is to change this into two (or more?) 
separate processes (tricky).
"""


from iface import IFace
from lattice import Lattice
from rule import Rule
from itset import ItSet
from math import isfinite
from heapq import heappush
from iter_subsets import all_proper_subsets


class PartRulMiner:

    def _set_m_impr(self, rul, la):
        if rul.cn.suppratio < IFace.hpar.abs_suppratio:
            IFace.reporterror(" .. low suppratio, should not happen anymore " + str(rul))
        altconf = 0
        cl_ants = set([])
        for an2 in la.allpreds(rul.an):
            cn2 = la.miner.close(rul.rcn.union(an2))
            if (cf := cn2.supp/an2.supp) > altconf:
                altconf = cf
            if rul.conf < IFace.hpar.abs_m_impr * altconf:
                rul.cboo = altconf # only an upper bound but discarded
                return False
        if altconf > 0:
            rul.m_impr = rul.conf/altconf # not discarded, correct value
        elif isfinite(rul.cn.suppratio):
            "Empty antecedent, only suppratio."
            rul.m_impr = float("inf")
        else:
            "No m_impr and no suppratio: can't evaluate that rule"
            print(" .. discarding", rul, "no m_impr, no suppratio")
            return False
        rul.set_cboo()
        return True

    def mine_partial_rules(self, latt, cn):
        for an in latt.allpreds(cn): 
            rul = Rule(an, cn)
            if rul.conf > IFace.hpar.confthr and \
               self._set_m_impr(rul, latt):
                yield rul




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

    def set_m_impr(self, rul, miner):
        "rul assumed to be an implication, test std (non-closure) mult impr"
        if rul.conf < 1:
            IFace.reporterror("Multiplicative improvement test expected" +
                " an implication but got instead " + str(rul))
        if rul.cn.suppratio < IFace.hpar.abs_suppratio:
            IFace.reporterror(" .. low suppratio, should not happen anymore " + str(rul))
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
            if cn2.supp * IFace.hpar.abs_m_impr > an2cl.supp:
                # ~ print(" .. discarding", rul, an2, cn2, cn2.supp / an2cl.supp)
                return False
            if cn2.supp > altconf * an2cl.supp:
                altconf = cn2.supp / an2cl.supp
        if altconf > 0:
            rul.m_impr = 1/altconf
        elif isfinite(rul.cn.suppratio):
            "Empty antecedent, only suppratio."
            rul.m_impr = float("inf")
        else:
            "No m_impr and no suppratio: can't evaluate that rule"
            print(" .. discarding", rul, "no m_impr, no suppratio")
            return False
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





class RuleMiner: 

    def __init__(self, hpar, dataset, supprat = True):
        "some codes, reserved rules, and average lift so far"
        self.latt = Lattice(dataset)
        if not supprat:
            self.latt.boosthr = 1 # SHORTCIRCUIT SUPPRATIO CONSTRAINT PUSH
        self.count = 0
        self.im = ImplMiner()
        self.prm = PartRulMiner()

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
                for rul in self.prm.mine_partial_rules(self.latt, cn):
                    self.count += 1
                    yield rul


if __name__=="__main__":

    from hyperparam import HyperParam
    from filenames import FileNames
    from dataset import Dataset

##    fnm = "pumsb_star"
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
    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"
    # ~ fnm = "../data/votesTr" 
    # ~ fnm = "../data/NOW" 
    # ~ fnm = "../data/papersTr"   # FILLS 15GB VERY EASILY
    # ~ fnm = "../data/chess.td"   # Fills 8GB with small heap size
    fnm = "../data/connect.td" # Fills 8GB with ridiculous heap
                                   # size and less than 5000 closures
                                   # but actually no associations found
                                   # and lattice minsupp still at inf

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
    if input(f"Show {len(rulist)} associations? "):
        for cnt, rul in enumerate(sorted(rulist, 
              key = lambda r: r.cboo, reverse = True)):
            print(cnt + 1, "/", rul, rul.cn.suppratio, rul.m_impr)


