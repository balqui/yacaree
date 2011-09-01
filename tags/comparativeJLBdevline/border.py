class Border:
    """
    Implements the iPred variant of the
    border algorithm to construct FCA closure lattices
    """

    def __init__(self):
        """
        it receives now the lattice (version 1.0 did not)
        contents: list of sets in the current cover
        emptyclos: closure of the empty set in the lattice
        lowcovun, auxiliary dict: for x, union of lower covers of x seen so far
        """
        self.contents = []
        self.lowcovun = {}
        self.emptyclos = None

    def record_clos_empty(self,emptyclos):
        self.emptyclos = emptyclos

    def append(self,e):
        "should subclass list when upgrading to Python 3"
        self.contents.append(e)

    def cover_update(self,e,latt):
        """
        return all covers of e and take them out of the border
        do not distinguish anymore candidates that were already in the border
        lattice needed to get intersection as a closure
        """
        self.lowcovun[e] = self.emptyclos
        candidates_in = []
        candidates_out = set([])
        cover = []
        newborder = []
        for ee in self.contents:
            if ee <= e:
                "intersection is border element, potential cover"
                candidates_in.append(ee)
            else:
                "potential cover is proper subset intersection"
                rr = set(ee.intersection(e))
                r = latt.close(rr)
                candidates_out.add(r)
                newborder.append(ee)
        for ee in candidates_in:
            "pick maxima, return the others back to the border"
            for eee in list(candidates_out) + candidates_in:
                if ee < eee:
                    "is this really possible? I think I proved NOT"
                    newborder.append(ee)
                    break
            else:
                "no larger candidate"
                cover.append(ee)
        for ee in candidates_out:
            "pick maxima, discard the others"
            for eee in list(candidates_out) + candidates_in:
                if ee < eee:
                    break
            else:
                "no larger candidate"
                cover.append(ee)
        self.contents = newborder
        return cover

if __name__ == "__main__":

    class pseudolatt():
        "stub to test Border with plain intersections"
        def __init__(self):
            pass
        def close(self,a):
            return frozenset(a)

    c = pseudolatt()
    
    b = Border()
    b.append(set(['a']))
    b.append(set(['b','c']))
    b.append(set(['c','d']))
    b.append(set(['d','e']))
    print b.contents
    print b.cover_update(set(['a','b','c']),c)
    print b.contents
    
