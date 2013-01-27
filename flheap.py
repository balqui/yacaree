"""
A somewhat more flexible heap (priority queue) where the
priority of each element is computed by a member function.
This priority function defaults to identity. 

Additionally exhibits a stub function for element size.
Keeps length and "total size sum" according to it.
Member functions .pr() (for priority) and .elemsize()
are expected to be overriden by FlHeap subclasses.

The outcomes of the .pr() overriding function must allow 
comparison according to a total order.

This implementation uses heapq operations from the standard
library; an alternative implementation may use in the future
the HeapDict class.

On Python 3 this should be a subclass of list so that, for
a FlHeap h, one can iterate just using "while h:" instead
of calling h.more().

"""

from heapq import heappush, heappop

class FlHeap:

    def __init__(self):
        self.storage = []
        self.count = 0
        self.totalsize = 0

    def pr(self,elem):
        return elem

    def elemsize(self,elem):
        return 0

    def push(self,elem):
        "push an elem into the heap, paired up with its pr"
        self.count += 1
        self.totalsize += self.elemsize(elem)
        heappush(self.storage,(self.pr(elem),elem))

    def mpush(self,elemslist):
        """
        multipush: push all elems from an iterable
        into the heap, each paired up with its pr
        (might be convenient instead to program this and
        call from push with a singleton list?)
        """
        for e in elemslist:
            self.push(e)

    def pop(self):
        "discard component [0] as it is the pr"
        nextel = heappop(self.storage)
        nextel = nextel[1]
        self.count -= 1
        self.totalsize -= self.elemsize(nextel)
        return nextel

    def more(self):
        "boolean from list - this should become deprecated at some point"
        return self.storage

if __name__ == "__main__":
    "MUST ADD TESTS FOR THE SIZES AND COUNTS"

    class FlHeapA(FlHeap):

        def __init__(self):
            FlHeap.__init__(self)

        def pr(self,elem):
            "priority overriding by hash"
            return hash(elem)

    class FlHeapB(FlHeap):

        def __init__(self):
            FlHeap.__init__(self)

        def pr(self,elem):
            "overriding by sign change on first component as in yaFlHeap"
            return -elem[0]

    numheapmin = FlHeapA()

    numheapmin.mpush([6,1,5,5,4,6,2,1,2])

    test = []

    while numheapmin.more():
        test.append(numheapmin.pop())

    if test == [1,1,2,2,4,5,5,6,6]:
        pass
    else:
        print "expected [1,1,2,2,4,5,5,6,6], obtained", test

    numheapmax = FlHeapB()

    for e in [6,1,5,5,4,6,2,1,2]:
        numheapmax.push([e])

    test = []

    while numheapmax.more():
        test.append(numheapmax.pop())

    if test == [ [e] for e in [6,6,5,5,4,2,2,1,1] ]:
        pass
    else:
        print "expected singletons from [6,6,5,5,4,2,2,1,1], obtained", test

    h = FlHeapA()

    h.mpush("all the letters of this sentence")

    test = ""

    while h.more():
        test += h.pop()

    if test == "ac     eeeeeefhhilllnnorsssttttt":
        pass
    else:
        print "expected 'ac     eeeeeefhhilllnnorsssttttt', obtained", test
    
