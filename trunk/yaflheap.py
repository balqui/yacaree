"""
yacaree particular subclass of FlHeap

Overrides priority with sign change of projection on 0th
component, which will be the support of the closure.

We also have an extra operation test_size() that halves
the heap if it has grown too much.
"""

import statics

import flheap

from heapq import heappop, heapify

class FlHeap(flheap.FlHeap):

    def __init__(self):
        flheap.FlHeap.__init__(self)

    def pr(self,elem):
        "overriding by sign change on first component"
        return -elem[0]

    def elemsize(self,elem):
        return 1 + len(elem[1]) + len(elem[2])

    def test_size(self):
        """
        this initialization of current_supp is an ugly hack,
        uses that actually current_supp along will be negative
        to keep and transmit intsupp unchanged if heap unmodified
        """
        intsupp = 0
        if (self.count > statics.pend_len_limit or
            self.totalsize > statics.pend_total_limit or
            self.pend_clos_size(self.storage) > statics.pend_mem_limit):
            """
            too many closures pending expansion: raise
            the support bound so that about half of the
            pend_clos heap becomes discarded
            """
            lim = self.count / 2
            current_supp = self.storage[0][0]
            current_supp_clos = []
            new_pend_clos = []
            new_total_size = 0
            new_count = 0
            popped_count = 0
            while self.storage:
                b = heappop(self.storage)
                popped_count += 1
                if popped_count > lim: break
                if b[0] == current_supp:
                    current_supp_clos.append(b)
                else:
                    current_supp = b[0]
                    intsupp = -current_supp
                    for e in current_supp_clos:
                        new_count += 1
                        new_total_size += self.elemsize(e[1])
                    new_pend_clos.extend(current_supp_clos)
                    current_supp_clos = [b]
            self.storage = new_pend_clos
            self.count = new_count
            self.totalsize = new_total_size
        return intsupp

    def pend_clos_size(self,pend_clos):
        "for the time being - just deactivates one of the 3 tests"
        return 0

##    def pend_clos_size(self,pend_clos):
##        "by memory size, should try to spare recomputing it so often"
##        m = sys.getsizeof(pend_clos)
##        for b in pend_clos:
##            m += (sys.getsizeof(b[0]) +
##                  sys.getsizeof(b[1]) +
##                  sys.getsizeof(b[2]))
##        return m

##    def pend_clos_size(self):
##        "by lengths, insufficient for dense or big datasets"
##        m = len(self.pend_clos)
##        for pend in self.pend_clos:
##            m += len(pend[1]) + len(pend[2])
##        return m




if __name__ == "__main__":
    "must create a true test set here"

    clheap = FlHeap()

    clheap.push([3,[3,5],[6,7]])

    clheap.push([2,[2,4,5],[6,7]])

    clheap.push([4,[4,5],[6,7]])

    print clheap.totalsize
    print clheap.count
    print clheap.pop()
    print clheap.totalsize
    print clheap.count
    print clheap.pop()
    print clheap.pop()

    
