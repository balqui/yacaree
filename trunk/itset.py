class ItSet(frozenset):
    """
    itemsets are frozensets so that they can index dicts
    earlier they had supp, but now moved off to a dict in Lattice
    """

    def __init__(self,contents=[]):
        """
        tried
        frozenset.__init__(self,contents)
        but seems inappropriate
        """
        self = frozenset(contents)

    def __str__(self,trad={}):
        """
        prettyprint of itemset: support omitted if zero
        ToDo: handle optional element translator trad
        """
        s = ""
        for el in sorted(self):
            if  el in trad.keys():
                el = trad[el]
            if s=="":
                s = str(el)
            else:
                s += "," + str(el)
        s = "{ " + s + " }"
        return s

if __name__=="__main__":

    st = itset(range(5))
    print st

    

