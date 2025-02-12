# ORIGINALLY FILE troppus02.py AS DESCRIBED IN late_pluviose.txt


# ~ from suppcounter import SuppCounter
from dataset import Dataset
import flheap_old_repe as flheap
import argparse

SuppCounter = Dataset


class FlHeap(flheap.FlHeap):
    def __init__(self):
        flheap.FlHeap.__init__(self)

    def pr(self, elem):
        "overriding by sign change on first component"
        return -elem[0]


class ClMiner:
    """
    Troppus mining algorithm for mining closures in decreasing support

    Attributes:
        id (str): Miner ID
        d (SuppCounter): dataset encapsulated by SuppCounter
        pend (FlHeap): closures pending to be traversed

    """

    def __init__(self, d):
        "init heap"
        self.id = "troppus-improved"
        self.d = d
        initpend = d.nrtr, d.close([])
        self.pend = FlHeap()
        self.pend.push(initpend)

    def dec_supp_cl(self):
        while self.pend.more():
            clos = self.pend.pop()
            yield clos  # pair (support,closure)
            first_level = False  # unless we find otherwise later on
            mxsupp = 0
            pclos = [i for i in clos[1]]  # mutable copy of closure
            # Iterating with reverse we start with highest support closure
            for i in reversed(self.d.items):
                if first_level:
                    "set at previous loop: no further i can clear mxsupp"
                    break
                if i in pclos:
                    "remove this i as required for all future i's"
                    pclos.pop()
                else:
                    nst = pclos * 1  # copy to modify
                    nst.append(i)
                    sp = self.d.count(nst)
                    # ncl = self.d.close(nst) # moved off
                    if not pclos:
                        "nst a singleton: back down to singletons level"
                        first_level = True
                    if sp > mxsupp:
                        ncl = self.d.close(nst)  # bring here for improvement
                        for j in ncl:
                            if (j not in clos[1] and
                                    self.d.before((i,), (j,))):
                                break
                        else:
                            if sp > clos[0]:
                                break
                            else:
                                self.pend.push((sp, ncl))
                                mxsupp = sp


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', default="../data/paperExample.txt", help="Dataset to be used.")
    parser.add_argument('-s', '--support_threshold', type=int, default=1, help="Minimum support threshold.")
    args = parser.parse_args()

    miner = ClMiner(SuppCounter(args.dataset))

    #    allclos = []
    cnt = 0
    for e in miner.dec_supp_cl():
        if e[0] < args.support_threshold:
            print("Breaking at safety support %s" % args.support_threshold)
            break
        cnt += 1
        #        allclos.append((e[1],hash(frozenset(e[0])),e[0]))
        print("%s / (%s)%s" % (cnt, e[0], e[1]))
