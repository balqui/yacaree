"""
Current date: early Ventose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Closure miner based on the Troppus algorithm.

In the current version, the dict order does not coincide with
the yield order as nonclosed sets keep being added to the dict
along the way. Might consider restricting it to closures one day.

CAVEAT: MUST REVIEW SEVERAL THINGS MARKED "CAVEAT".
"""


from iface import IFace
from itset import ItSet
from dataset import Dataset

from heapq import heapify, heappush, heappop

from psutil import virtual_memory as vmem

from collections import Counter # consider removing this

class Test_Memory:

    def __init__(self, nrits):
        self.cuts = 0
        self.nrits = nrits
        self.nrits_thr = 1000
        self.first_thr = 50
        self.secnd_thr = 65
        self.third_thr = 80

    def too_much_mem(self):
        if self.nrits < self.nrits_thr or self.cuts == 0:
            return vmem().percent > self.first_thr
        elif self.cuts == 1:
            return vmem().percent > self.secnd_thr
        else:
            "CAVEAT: third threshold or second?"
            return vmem().percent > self.third_thr

class ClMiner(dict):
    """
    Troppus-based miner. It is a dict from (frozen)sets of items 
    (closed or not) to their closing ItSet's. Has a mine_closures 
    generator of course to be called from Lattice.
    """

    def __init__(self, dataset, supp=-1):
        super().__init__()
        self.dataset = dataset
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        self.card = 0
        self.totlen = 0
        self.iface = IFace()
        self.pend_clos = list()
        self.mem_tester = Test_Memory(IFace.hpar.nrits)
        
        # ~ self.ctr = Counter()


    def supp_adding(self, itst, nitt):
        """
        Find support of the result of adding nitt (new item) to itst.
        If necessary, compute supporting set for that. Store on self 
        if not there yet. (THEN dict order is NOT yield order anymore.)
        Leave sets and closures in the dict even if their support is 
        zero.
        They are not that useful but wanted to avoid testing them again,
        grab a lot of memory though since closure is all the items.
        """
        exact = False # matches maybe a transaction
        itst = frozenset(itst)
        itstadd = frozenset(itst.union(nitt))
        if itstadd in self:
            "supp of union is supp of its closure"
            # ~ self.ctr["found as such"] += 1
            # ~ if self[itstadd].supp == 0:
                # ~ self.ctr["null support"] + 1
            return self[itstadd].supp
        if itst in self:
            "itstadd not in self but itst is, intersect support sets"
            # ~ self.ctr["filtered new item"] += 1
            supp = set(self[itst].supportset) & nitt.supportset
            clos = self.dataset.inters(supp)
        else:
            "need to compute support set on data"
            supp, exact = self.dataset.slow_supp(itstadd)
            if exact:
                "matched a transaction hence it is closed"
                # ~ self.ctr["matched a transaction"] += 1
                clos = itstadd
            else:
                "intersect support sets"
                # ~ self.ctr["intersected transactions"] += 1
                clos = self.dataset.inters(supp)
        clos = ItSet(clos, supp)
        # ~ if clos.supp > 0:
        self[itstadd] = clos
        self.totlen += len(supp)
        # ~ if clos.supp == 0:
            # ~ self.ctr["null support"] + 1
        return clos.supp


    def test_size(self):
        """
        Similar to test_size in yaflheap, with the so-called ugly hack, 
        but now for a standard heap kept in a standard list; other
        than that, very close to version 1.*.
        """
        intsupp = 0 # return 0 if supp unchanged o/w return new supp
        # ~ if ((count := len(self.pend_clos)) > IFace.hpar.pend_len_limit
          # ~ or self.totlen > IFace.hpar.tot_len_limit):
            # ~ """
            # ~ Too many closures pending expansion: raise
            # ~ the support bound so that about half of the
            # ~ heap becomes discarded. Careful that support-tied
            # ~ ItSet's are either all kept or all discarded.
            # ~ Trying to control as well tot_len_limit.
            # ~ """
        incr_supp = False
        if self.mem_tester.too_much_mem():
            IFace.report("Too high memory usage: " + 
                "increasing support threshold.")
            incr_supp = True
        if len(self.pend_clos) > IFace.hpar.pend_len_limit:
            IFace.report("Too many pending closures: " + 
                "increasing support threshold.")
            incr_supp = True
        if incr_supp:
            """
            Lowish amount of system's memory remains available. 
            Often, however, most memory is not employed by the heap
            (e.g. the closures dict instead): maybe, cutting away 
            half the heap does not free much. But the new support 
            may allow the computation to complete anyway.
            """
            self.mem_tester.cuts += 1
            lim = len(self.pend_clos) // 2
            current_supp = self.pend_clos[0].supp
            current_supp_clos = []
            new_pend_clos = []
            new_count = 0
            popped_count = 0
            while self.pend_clos:
                itst = heappop(self.pend_clos)
                popped_count += 1
                if popped_count > lim: break
                if itst.supp == current_supp:
                    current_supp_clos.append(itst)
                else:
                    intsupp = current_supp
                    new_pend_clos.extend(current_supp_clos)
                    current_supp = itst.supp
                    current_supp_clos = [itst]
            self.pend_clos = new_pend_clos
        return intsupp


    def mine_closures(self):
        "As per the Troppus algorithm"

        IFace.report("Memory control on closure miner via psutil.")
        closempty = set()
        sorteditems = list()

        for it in self.dataset.univ:
            if len(self.dataset.occurncs[it]) == self.dataset.nrtr:
                closempty.add(it)
            else:
                sorteditems.append(
                    ItSet([it], self.dataset.occurncs[it])
                )

        sorteditems.sort() # decr supp, item tie-break, see ItSet.__lt__

        closempty = ItSet(closempty, range(self.dataset.nrtr))
        self.pend_clos = [ closempty ]

        report_it = False
        self.minsupp = self.dataset.nrtr
        while self.pend_clos and self.iface.running:
            """
            Yield next closure and handle extensions.
            CAVEAT: IFace.running condition still fully untested.
            """
            clos = heappop(self.pend_clos)
            pclos = set(clos)  # mutable copy of contents
            if frozenset(pclos) not in self:
                self[frozenset(pclos)] = clos
            self.card += 1
            yield clos

            if self.card % IFace.hpar.check_size_often == 0:
                "Consider raising support."
                new_supp = self.test_size()
                if new_supp > self.intsupp:
                    "support bound grew, heap halved, report"
                    IFace.report(
                      f"Increased minimum support from {self.intsupp} "
                      + f"({self.intsupp*100/self.dataset.nrtr:5.3f}%) "
                      + f"up to {new_supp} " 
                      + f"({new_supp*100/self.dataset.nrtr:5.3f}%).")
                    self.intsupp = new_supp
                    report_it = True
            if self.card % IFace.hpar.report_often == 0 or report_it:
                "Just report."
                report_it = False
                IFace.report(
                  f"{self.card} closures traversed, " +
                  f"{len(self.pend_clos)} further closures " +
                  f"found so far; current support {clos.supp}.")

            first_level = False  # unless we find otherwise later on
            mxsupp = 0
            for itt in sorteditems:
                (i,) = itt # extract the item in the singleton ItSet
                # ~ if first_level:
                    # ~ """
                    # ~ set at previous loop: no further i can clear mxsupp
                    # ~ CAVEAT: I don't fully understand these conditions
                    # ~ """
                    # ~ break
                if i in pclos:
                    "remove this i as required for all future i's"
                    pclos.remove(i)
                else:
                    nst = pclos.copy() # copy to modify
                    sp = self.supp_adding(nst, itt)
                    if not pclos:
                        """
                        nst a singleton: back down to singletons level
                        CAVEAT: I don't fully understand these conditions
                        """
                        first_level = True
                    if sp > mxsupp:
                        ncl = self[frozenset(nst.union(itt))]
                        for j in ncl:
                            jtt = ItSet({j}, self.dataset.occurncs[j])
                            # ~ if (j not in clos and
                               # ~ (itt.supp > jtt.supp or
                               # ~ (itt.supp == jtt.supp and i > j))):
                            if (j not in clos and itt < jtt):
                                "CAVEAT: I don't fully understand these conditions"
                                # ~ print(" --- discard as:", jtt, ">", itt)
                                break
                        else:
                            if sp > clos.supp:
                                break
                            elif sp > self.intsupp:
                                heappush(self.pend_clos, ncl)
                                mxsupp = sp

    def close(self, st):
        "find (and store if new) closure of set st"
        fst = frozenset(st)
        if fst in self:
            "self expected to contain already the whole closure space"
            return self[fst]
        supp, exact = self.dataset.slow_supp(fst)
        if exact:
            "matched a transaction hence it is closed"
            clos = fst
        else:
            "intersect support sets"
            clos = self.dataset.inters(supp)
        clos = ItSet(clos, supp)
        # ~ if clos.supp > 0:
        self[fst] = clos
        self.totlen += len(supp)
        return clos


if __name__ == "__main__":

    from filenames import FileNames
    from hyperparam import HyperParam
    from time import time

    fnm = "../data/markbask"

    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/ect24.td"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e5b"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"
    # The next work thanks to the limit on the total support set lengths / NOT IMPLEMENTED ANYMORE
    # ~ fnm = "../data/chess.td"   # Fills memory with small heap size
    # ~ fnm = "../data/connect.td" # Fills memory with ridiculous heap
                                   # size and less than 5000 closures
    # ~ fnm = "../data/mushroomTr" 
    # ~ fnm = "../data/votesTr" 
    # ~ fnm = "../data/papersTr" # FILLS 15GB MEMORY ANYHOW EVEN WITH THE TOTAL SUPPORT SET LENGTHS LIMIT

    IFace.hpar = HyperParam()
    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()

    # ~ miner = ClMiner(d, 0.084)
    # ~ miner = ClMiner(d, 0.75)
    # ~ miner = ClMiner(d, 3/24)
    # ~ import time
    miner = ClMiner(d, 0)
    # ~ print("Int support:", miner.intsupp)
    lcl = list()
    # ~ t0 = time.time()
    for cl in miner.mine_closures():
        lcl.append(cl)
        # ~ if miner.card > IFace.hpar.clos_num_limit:
        # ~ if len(lcl) == 2000:
            # ~ break
        # ~ print(cl)
    # ~ t1 = time.time()
    # ~ print(t1 - t0)
    print(f"Number of closures: {len(lcl)} of " + 
          f"support {cl.supp} of more; total lengths {miner.totlen}, {miner.card}.") # or miner.card

# ~ Counter of various classes of closures, uncomment self.ctr in __init__
    # ~ rrr = 0
    # ~ for c in miner.ctr:
        # ~ print(c, miner.ctr[c])
        # ~ rrr += miner.ctr[c]
    # ~ print("%:", miner.ctr["intersected transactions"]*100/rrr)

    # ~ for cl in lcl:
        # ~ print(' '.join(e for e in sorted(cl)))
        # ~ print(cl)




    # ~ a = set(['D', 'E'])
    # ~ print("Closure of", a, "is", miner.close(a))



    # ~ print("In dict:")
    # ~ for fs in miner:
        # ~ if miner[fs].supp == 0:
            # ~ print(fs, miner[fs])


# Reporting and support increase fragments from V1.*, PROBABLY TO REMOVE
            # ~ new_supp = test_size(pend_clos)
            # ~ if new_supp > self.intsupp:
                # ~ "support bound grows, heap halved, report"
                # ~ IFace.report("Increasing min support from " +
                             # ~ str(self.intsupp) +
                             # ~ (" (%2.3f%%) up to " %
                              # ~ self.to_percent(self.intsupp)) +
                             # ~ str(new_supp) +
                             # ~ (" (%2.3f%%)" %
                              # ~ self.to_percent(new_supp)) + 
                            # ~ ".")
                # ~ IFace.hpar.please_report = True
                # ~ self.intsupp = new_supp
            # ~ if spp < self.intsupp:
                # ~ "maybe intsupp has grown in the meantime (neg border)"
                # ~ break
            # ~ if spp < self.minsupp:
                # ~ self.minsupp = spp
            # ~ if (IFace.hpar.verbose or IFace.hpar.please_report or 
                # ~ self.card % IFace.hpar.supp_rep_often == 0):
                # ~ IFace.hpar.please_report = False
                # ~ IFace.report(str(self.card) +
                            # ~ " closures traversed, " +
                               # ~ str(len(pend_clos)) + 
                            # ~ " further closures found so far; current support " +
                            # ~ str(spp) + ".")

        # ~ This leads to wrong answers in the linear search attempt,
        # ~ took them out, now putting them back in.
        # ~ for clos in self.values():
            # ~ "linear search - TAKEN OUT, several points add to the dict and arrival order is not yield order"
            # ~ if fst <= clos:
                # ~ "dict order: largest-support closure containing fst"
                # ~ self[fst] = clos
                # ~ return clos
        # ~ "or fall back on dataset - which is slower?"
