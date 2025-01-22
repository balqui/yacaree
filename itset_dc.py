"""
Aux tests for yacaree

Early Pluviose 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Consider migrating it into a frozen dataclass.

NEED TO LEARN ABOUT __slots__ AND __new__
(write to JD about the "trickyness" in 
https://docs.python.org/3/glossary.html#term-__slots__)
"""

from dataclasses import dataclass, field

@dataclass(frozen = True)
class ItSet:
	contents: set
	supportset: set = field(default_factory=set)
	supp: int = -1
	suppratio: float = float("inf")
	tie_breaker: int = 0

	def __post_init__(self):
		if self.supp < 0 and self.supportset:
			self.supp = len(self.supportset) # and now handle the tie breaker

	def __eq__(self, other):
		pass

	@classmethod
	def _adv_cnt(cls):
		pass



    # ~ cnt = 0 # counts created ItSet's to set up the tie_breaker

    # ~ def __init__(self, contents = set(), supportset = []):
        # ~ """
        # ~ Current closure miner puts in heap pending closures with
        # ~ their supporting set of transactions. Maybe one day I can
        # ~ bet rid of that list and store only the support but, as of
        # ~ today, I keep it.
        # ~ """
        # ~ super().__init__(contents)
        # ~ self._hash = hash(frozenset(contents))
        # ~ self.supportset = supportset
        # ~ self.supp = len(supportset)
        # ~ self.suppratio = float("inf") # default
        # ~ ItSet.cnt += 1
        # ~ self.tie_breaker = ItSet.cnt
        # ~ ## print(" *** created:", self, self.supportset, self.tie_breaker)

    # ~ def __lt__(self, other):
        # ~ """
        # ~ For heap purposes, ItSet-smaller itemsets will come out first,
        # ~ hence these must be the ones with larger supports. Support ties
        # ~ are broken arbitrarily by creation time order.  
        # ~ Order comparisons must not see ever the contents,
        # ~ as set comparison is not total.
        # ~ CAVEAT: a == b acts in <= and >= as contents set equality. 
        # ~ """
        # ~ return (self.supp > other.supp or
                # ~ self.supp == other.supp and
                    # ~ self.tie_breaker < other.tie_breaker)

    # ~ def __lshift__(self, other):
        # ~ """
        # ~ Use "<<" instead to compare ItSet's according to inclusion
        # ~ order on the contents.
        # ~ """
        # ~ return set(self) <= set(other)

    # ~ def __hash__(self):
        # ~ """
        # ~ Try to make it hashable so that they can be in set's and
        # ~ index dict's exactly as the frozenset of the contents.
        # ~ """
        # ~ return self._hash

    # ~ def __str__(self):
        # ~ return ('{ ' + ', '.join(sorted(str(e) for e in self)) +
                       # ~ ' } [' +  str(self.supp) + ']')

    # ~ def difference(self, anything):
        # ~ "returns a plain set, not an ItSet, as we lack supp"
        # ~ return self - set(anything)

# ~ if __name__ == "__main__":

    # ~ ## PENDING: test printing and all the comparisons with all cases, also difference

    # ~ print(ItSet([], range(100, 120)))
    # ~ s0 = ItSet([], range(100, 120))
    # ~ print(s0)
    # ~ s1 = ItSet([], range(150, 175))
    # ~ print(s1)
    # ~ print(ItSet(range(5), range(200, 210)))
    # ~ s2 = ItSet(range(5), range(200, 210))
    # ~ print(s2)

    # ~ print("s0 == s1", s0 == s1)
    # ~ print("s0 == s2", s0 == s2)
    # ~ print("s2 == s1", s2 == s1)

    # ~ a = ItSet(range(5), range(30))
    # ~ print("s1", s1)
    # ~ print("s2", s2)
    # ~ print("a", a)
    # ~ print("s2 < a", s2 < a)
    # ~ print("a < s2", a < s2)
    # ~ print("s2 > a", s2 > a)
    # ~ print("set(s2) == set(a)", set(s2) == set(a))
    # ~ print("s2 == a", s2 == a)
    # ~ print("set(s2) < set(a)", set(s2) < set(a))
    # ~ print("set(s2) <= set(a)", set(s2) <= set(a))
    # ~ print("s2 << a", s2 << a)
    # ~ print("a << s2", a << s2)

    # ~ print("s0 found in [s1, s2]?", s0 in [s1, s2])

    # ~ b = a.difference([2, 3])
    # ~ print(b, type(b))

    # ~ print(set([s0, s1, s2, a]))
