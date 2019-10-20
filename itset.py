class ItSet(frozenset):
    """
    itemsets are frozensets so that they can index dicts
    earlier they had supp, but now moved off to a dict in Lattice
    Tried several things and also followed up this, but to no avail:
    http://infamousheelfilcher.blogspot.com/2012/09/subclassing-immutable-types-in-python-3.html
    """

    def __init__(self,contents=[]):
        """
        frozenset.__init__(self,contents)
        did not work with Python 2, did instead
        self = frozenset(contents)
        """
        self = frozenset(contents)

    def __str__(self,trad={}):
        """
        prettyprint of itemset: support omitted if zero
        ToDo: handle optional element translator trad
        """
        sep = ""
        s = ""
        for el in sorted(self):
            if  el in trad.keys():
                el = trad[el]
            if s=="":
                s = str(el)
            else:
                s += sep + str(el)
            sep = ", "
        s = "{ " + s + " }"
        return s

if __name__=="__main__":

    st = ItSet(range(5))
    print(st)

    

