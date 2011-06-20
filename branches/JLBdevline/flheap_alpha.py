"""
A somewhat more flexible heap (priority queue) where the
priority of each element is computed by a custom function.

Keeps length and, if a size function for elements is
available, also total size sum.

The priority function defaults to identity. The outcomes
of the custom priority function must allow comparison according
to a total order.

This version receives custom priority and element size as
parameters upon initialization.

This implementation uses heapq operations from the standard
library; an alternative implementation may use in the future
the HeapDict class.

On Python 3 this should be a subclass of list so that, for
a FlHeap h, one can iterate just using "while h:" instead
of calling h.more().

"""

from heapq import heappush, heappop

def _FlHeap__defaultpriority(elem):
        "default for how to compute the priority of an element"
        return elem

def _FlHeap__defaultelemsize(elem):
        "default for how to compute the size of an element"
        return 0

class FlHeap:

    def __init__(self,
                 custompriority = __defaultpriority,
                 elemsize = __defaultelemsize):
        self.storage = []
        self.count = 0
        self.totalsize = 0
        self.pr = custompriority
        self.elemsize = elemsize

    def push(self,elemslist):
        "push an iterable of elems into the heap, each paired up with its pr"
        for e in elemslist:
            self.count += 1
            self.totalsize += self.elemsize(e)
            heappush(self.storage,(self.pr(e),e))

    def pop(self):
        "discard component [0] as it is the pr"
        nextel = heappop(self.storage)[1]
        self.count -= 1
        self.totalsize -= self.elemsize(nextel)
        return nextel

    def more(self):
        "boolean from list - this should become deprecated at some point"
        return self.storage

if __name__ == "__main__":
    "MUST ADD TESTS FOR THE SIZES AND COUNTS AND THAT"

    def hashprio(e):
        return hash(e)

    def negcompprio(e):
        "like the one used in the subclass in yaFlHeap"
        return -e[0]

    numheapmin = FlHeap()

    numheapmin.push([6,1,5,5,4,6,2,1,2])

    test = []

    while numheapmin.more():
        test.append(numheapmin.pop())

    if test == [1,1,2,2,4,5,5,6,6]:
        pass
    else:
        print "expected [1,1,2,2,4,5,5,6,6], obtained", test

    numheapmax = FlHeap(negcompprio)

    listsingletons = [ [e] for e in [6,1,5,5,4,6,2,1,2] ]

    numheapmax.push(listsingletons)

    test = []

    while numheapmax.more():
        test.append(numheapmax.pop())

    if test == [ [e] for e in [6,6,5,5,4,2,2,1,1] ]:
        pass
    else:
        print "expected singletons from [6,6,5,5,4,2,2,1,1], obtained", test

    h = FlHeap(hashprio)

    h.push("all the letters of this sentence")

    test = ""

    while h.more():
        test += h.pop()

    if test == "ac     eeeeeefhhilllnnorsssttttt":
        pass
    else:
        print "expected 'ac     eeeeeefhhilllnnorsssttttt', obtained", test
    
