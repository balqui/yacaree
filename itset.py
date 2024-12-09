'''
yacaree

Current revision: mid / late Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

class ItSet(frozenset):
    """
    itemsets are frozensets so that they can index dicts;
    earlier they had supp, but later moved off to a dict in Lattice.
    (12/2024) Unclear what difference is relevant beyond a custom
    __str__ but will keep the class around anyhow for the time being.
    """

    def __init__(self, contents=[]):
        """
        frozenset.__init__(self, contents)
        did not work with Python 2 nor 3, and
        super().__init__(self, contents)
        did not work either.
        """
        self = frozenset(contents)

    def __str__(self, trad={}):
        """
        prettyprint of itemset: CAVEAT: add support if nonzero?
        ToDo: handle optional element translator trad
        """
        return "{ " + ', '.join( str(trad[el]) if el in trad else str(el)
                              for el in sorted(self) ) + " }"

if __name__=="__main__":
    print(ItSet(range(5)))

    

