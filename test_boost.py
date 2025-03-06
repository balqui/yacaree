'''
ancillary module for yacaree

Current revision: mid Ventose 2025

Programmers: JLB

'''

from rule import Rule
from iface import IFace

from iter_subsets import all_proper_subsets

from hytra import HyperGraph as hypergraph
from hytra import transv_zero as transv

def _faces(itst, listpred):
        "listpred immediate preds of itst - make hypergraph of differences"
        return hypergraph(itst, [ itst.difference(e) for e in listpred ])


def test_std(rul, miner):
    cb = rul.cn.suppratio
    cl_ants = set([])
    for an2 in all_proper_subsets(set(rul.an)):
        cl_ants.add(miner.close(an2))
    for an2 in cl_ants:
        "ToDo: refactor avoiding floats"
        cn2 = miner.close(rul.rcn.union(an2))
        if an2.supp == 0:
            pass
            print(" ...... in std, zero an support of", an2)
        elif cn2.supp == 0:
            # ~ pass
            print(" ...... in std, zero cn support of", cn2)
        else:
            if cn2.supp / an2.supp < cb:
                cb = cn2.supp / an2.supp
                # ~ print(" ...... std lower via", an2, cb)
    return cb


def test_cl(rul, miner):
    cb = rul.cn.suppratio
    cl_ants = set([])
    for an2 in all_proper_subsets(set(rul.cn)):
        "implication, closure of rul.an is rul.cn"
        an2cl = miner.close(an2)
        if len(an2cl) < len(rul.cn):
            cl_ants.add(an2cl)
    for an2 in cl_ants:
        "ToDo: refactor avoiding floats"
        cn2 = miner.close(rul.rcn.union(an2))
        if an2.supp == 0:
            print(" ...... in cl, zero an support of", an2)
            pass
        elif cn2.supp == 0:
            print(" ...... in cl, zero cn support of", cn2)
            pass
        else:
            if cn2.supp / an2.supp < cb:
                cb = cn2.supp / an2.supp
                # ~ print(" ...... cl lower via", an2, cb)
    return cb



def test(rul, miner):
    # ~ print(" .. testing", rul, end = ' ')
    if rul.cn.suppratio < IFace.hpar.absoluteboost:
        pass
        # ~ print(" .... low suppratio", rul)
    else:
        # ~ print(" .... init", rul.cn.suppratio)
        cl = test_cl(rul, miner)
        std = test_std(rul, miner)
        # ~ print(" .... closure based:", cl)
        # ~ print(" .... standard:", std)
        if std != cl:
            print(" .. DIFFERENCE IN", rul)
            print(" .... closure based:", cl)
            print(" .... standard:", std)
            exit(1)

def mine_implications(latt, cn):
    """
    Gets a closure cn, with suppratio if known: find implications there.
    If all supersets below minsupp, suppratio not known.
    CAVEAT: keep count somehow of discarded implications!
    """
    mingens = list( m for m in transv(_faces(cn, latt[cn])).hyedges )
    if not mingens:
        IFace.reportwarning("No minimum generators for " + 
            f"{str(cn)}, predecessors: [ " +
            f"{'; '.join(str(e) for e in latt[cn])} ]")
    if len(cn) == len(mingens[0]):
        "no rules as cn is a free set and its own unique mingen"
        pass
    else:
        for an in mingens:
            an = frozenset(an)
            if an in latt:
                "look it up on clminer instead"
                print(an, "ALREADY IN lattice, then something wrong I believe")
                exit(1)
            else: 
                "CAVEAT: pending to clarify which cboost and impose it"
                rul = Rule(an, cn, full_impl = True)
                # ~ if is_cboost_high_impl(rul, latt.miner):
                yield rul






if __name__=="__main__":

    from filenames import FileNames
    from hyperparam import HyperParam
    from lattice import Lattice
    from dataset import Dataset

    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/lenses_recoded.txt"
    # ~ fnm = "../data/cmc-full"

    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    # ~ fnm = "../data/e5b"
    # ~ fnm = "../data/e5"
    # ~ fnm = "../data/p5.td"

    # ~ fnm = "../data/papersTr" # FILLS 18.5GB MEMORY ANYHOW EVEN WITH THE TOTAL SUPPORT SET LENGTHS LIMIT, recommend supp 0.04, 0.025 almost requires 16GB
    fnm = "../data/votesTr" 
    # The next work thanks to the limit on the total support set lengths
    # ~ fnm = "../data/chess.td"   # Fills 8GB memory with small heap size
    # ~ fnm = "../data/connect.td" # Fills 8GB memory with ridiculous heap




    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

    la = Lattice(d)
    supp = 0
    impls = list()

    for cn in la.candidate_closures(supp): 

        if cn not in la:
            print("Lattice misses", cn)
            exit(1)

        if cn:
            for rul in mine_implications(la, cn):
                test(rul, la.miner)
                impls.append(rul)

    if input(f"Show {len(impls)} implications? "):
        for rul in impls:
            print(rul) # [0], "=>", rul[1].difference(rul[0]))

    if input("Show lattice? "):
        print("Lattice:")
        for a in la:
            print(a)

