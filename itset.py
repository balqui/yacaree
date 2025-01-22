"""
yacaree

Current revision: late Nivose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Careful: a hash is defined to use ItSet's as set members and 
dict keys; ItSet should be handled always as immutable even though
the program does not control that instances don't change.

A simplified version might be handy where we only keep contents 
and supp, forgetting supportset and suppratio once they have 
fulfilled their roles.

History:

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
Moreover, we need to compare ItSets according to two orderings,
support-based for the heap and mere subset order. We customize
"<" as support-based order for the heap and customize the "shift"
operator "<<" to mean instead the subset-or-equal relation.

Also: inheriting from frozenset does not work, since init requires
two parameters but somehow the instantiation mandates only one and
both one and two parameters raise errors. (Probably something to
do with __new__, maybe will try to find out some day.)

In Lattice I need to intersect ItSet's and use the outcome to index
a dict. I could give ItSet an intersect method but it would have to
construct unions of the lists of transactions, and it is unclear 
that this is needed. For the time being, I take them down to frozensets
at the time of intersecting.

Old:

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
as they are no longer to index the supports dict in lattice...
but they index other dict's and belong to other set's).
"""

# ~ from functools import total_ordering
# ~ @total_ordering 
# ~ Do we really need it?
# ~ Also, some preliminary experiments raise doubts whether
# ~ that decorator would work as I intend in this case.

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
        self._hash = hash(frozenset(contents))
        self.supportset = supportset
        self.supp = len(supportset)
        self.suppratio = 0 # placeholder for later
        ItSet.cnt += 1
        self.tie_breaker = ItSet.cnt
        # ~ print(" *** created:", self, self.supportset, self.tie_breaker)

    # ~ def __eq__(self, other):
        # ~ return self.contents == other.contents
        # ~ inherited from super instead

    def __lt__(self, other):
        """
        For heap purposes, ItSet-smaller itemsets will come out first,
        hence these must be the ones with larger supports. Support ties
        are broken arbitrarily by creation time order.  
        Order comparisons must not see ever the contents,
        as set comparison is not total.
        CAVEAT: a == b acts in <= and >= as contents set equality. 
        """
        return (self.supp > other.supp or
                self.supp == other.supp and
                    self.tie_breaker < other.tie_breaker)

    def __lshift__(self, other):
        """
        Use "<<" instead to compare ItSet's according to inclusion
        order on the contents.
        """
        return set(self) <= set(other)

    def __hash__(self):
        """
        Try to make it hashable so that they can be in set's and
        index dict's exactly as the frozenset of the contents.
        """
        return self._hash

    def __str__(self):
        return ('{ ' + ', '.join(sorted(str(e) for e in self)) +
                       ' } [' +  str(self.supp) + ']')

    def difference(self, anything):
        "returns a plain set, not an ItSet, as we lack supp"
        return self - set(anything)

if __name__ == "__main__":

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

    a = ItSet(range(5), range(30))
    print("s1", s1)
    print("s2", s2)
    print("a", a)
    print("s2 < a", s2 < a)
    print("a < s2", a < s2)
    print("s2 > a", s2 > a)
    print("set(s2) == set(a)", set(s2) == set(a))
    print("s2 == a", s2 == a)
    print("set(s2) < set(a)", set(s2) < set(a))
    print("set(s2) <= set(a)", set(s2) <= set(a))
    print("s2 << a", s2 << a)
    print("a << s2", a << s2)

    print("s0 found in [s1, s2]?", s0 in [s1, s2])

    b = a.difference([2, 3])
    print(b, type(b))

    print(set([s0, s1, s2, a]))
