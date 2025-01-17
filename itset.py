"""
yacaree

Current revision: late Nivose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Programmed as
class ItSet(frozenset) 
until Nivose 2025.

Itemsets were frozensets so that they can index dicts;
initially they had supp, later moved off to a dict in Lattice.
(12/2024) Unclear what difference is relevant beyond a custom
__str__ but will keep the class around anyhow for the time being.

(Jan/2025)
Next goal is to use them, essentially, as heap elements so that
the standard heapq library can be employed at face falue, thus
getting rid of FlHeap and yaFlHeap.
For this, they need to include their own support and also a
tie-breaking component to make sure that the heap never compares
the sets themselves.
First idea was to change the sign of the support so that the heaps
work as max-heaps but current decision is to hide that into custom
comparisons.

def __init__(self, contents=[], supp = float("inf")):
    frozenset.__init__(self, contents)
    did not work with Python 2 nor 3, and
    super().__init__(self, contents)
    did not work either.
    Programmed as
    self = frozenset(contents)

def __str__(self):
    prettyprint of itemset: CAVEAT: add support if nonzero?
    return "{ " + ', '.join( str(trad[el]) if el in trad else str(el)
                          for el in sorted(self) ) + " }"
if __name__=="__main__":
    print(ItSet(range(5)))

Had a version in @dataclass form, but required looking up
the contents field to operate and I decided to get back to
inheriting from set (try not no use frozensets initially
as they are no longer to index the supports dict in lattice).
"""

from functools import total_ordering
        
@total_ordering
class ItSet(set):

    cnt = 0 # counts created ItSet's to set up the tie_breaker

    def __init__(self, contents = set(), supportset = []):
        """
        Current closure miner puts in heap pending closures with
        their supporting set of transactions. Maybe one day I can
        bet rid of that list and store only the support but, as of
        today, I keep it.
        """
        super().__init__(contents)
        self.supportset = supportset
        self.supp = len(supportset)
        ItSet.cnt += 1
        self.tie_breaker = ItSet.cnt
        print(" *** created:", self)

    # ~ def __eq__(self, other):
        # ~ return self.contents == other.contents
        # ~ try to inherit from super instead

    def __lt__(self, other):
        """
        For heap purposes, ItSet-smaller itemsets will come out first,
        hence these must be the ones with larger supports. Support ties
        are broken arbitrarily by creation time order.  
        Order comparisons must not see ever the contents,
        as set comparison is not total.
        CAVEAT: a == b does not imply a <= b (nor a >= b either). 
        """
        return (self.supp > other.supp or
                self.supp == other.supp and
                    self.tie_breaker < other.tie_breaker)

    def __str__(self):
        return ('{ ' + ', '.join(str(e) for e in self) +
                       ' } [' +  str(self.supp) + ']')

    def difference(self, anything):
        "returns a plain set, not an ItSet, as we lack supp"
        return self - set(anything)

# ~ PENDING: test printing and all the comparisons with all cases, also difference

print(ItSet([], range(100, 120)))
s0 = ItSet([], range(100, 120))
print(s0)
s1 = ItSet([], range(150, 175))
print(s1)
print(ItSet(range(5), range(200, 210)))
s2 = ItSet(range(5), range(200, 210))
print(s2)

print("s0 == s1", s0 == s1)
print("s0 == s2", s0 == s2)
print("s2 == s1", s2 == s1)


a = ItSet(range(5), range(10))
b = a.difference([2, 3])
print(b, type(b))
