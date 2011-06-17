"""
A somewhat more flexible heap (priority queue) where the
priority of each element is computed by a custom function.

The priority function defaults to sign change of projection
on 0th component. To use the default, elements must be tuples
or lists and their 0th component must allow sign change and
comparison according to a total order; likewise, the outcomes
of the custom priority function must allow comparison according
to a total order.

This implementation uses heapq operations from the standard
library; an alternative implementation may use in the future
the HeapDict class.

On Python 3 this should be a subclass of list so that, for
a FlHeap h, one can iterate just using "while h:" instead
of calling h.more().

"""

from heapq import heappush, heappop

class FlHeap:

    def __defaultpriority(elem):
        return -elem[0]

    def __init__(self, custompriority = __defaultpriority):
        self.storage = []
        self.pr = custompriority

    def push(self,elemslist):
        "push an iterable of elems into the heap"
        for e in elemslist:
            heappush(self.storage,(self.pr(e),e))

    def pop(self):
        return heappop(self.storage)[1]

    def more(self):
        "boolean from list"
        return self.storage

if __name__ == "__main__":

    def hashprio(e):
        return hash(e)

    def idprio(e):
        return e

    numheapmin = FlHeap(idprio)

    numheapmin.push([6,1,5,5,4,6,2,1,2])

    test = []

    while numheapmin.more():
        test.append(numheapmin.pop())

    if test == [1,1,2,2,4,5,5,6,6]:
        pass
    else:
        print "expected [1,1,2,2,4,5,5,6,6], obtained", test

    numheapmax = FlHeap()

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
    
