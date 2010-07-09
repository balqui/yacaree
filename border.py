class Border:
    """
    to implement a couple of methods appropriate for the
    border algorithm to construct closure lattices
    maybe should become a subclass of list when this
    is doable
    """

    def __init__(self):
        "list of sets, initially empty"
        self.contents = []

    def append(self,e):
        "append one more set"
        self.contents.append(e)

    def cover_update(self,e,latt):
        """
        return all covers of e and take them out of the border
        distinguish candidates that were already in the border
        lattice needed to get intersection as a closure, maybe
        there is a better way
        TO REDO URGENTLY: remove print and rethink as per my notes
        """
##        print "cover-update for", e, "with border", self.contents
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
##                print "inters", ee, e, rr, r
                candidates_out.add(r)
                newborder.append(ee)
##        print "candidates in", candidates_in
##        print "candidates out", candidates_out
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
##        print "cover:", cover
##        print "new border:", newborder
        return cover

if __name__=="__main__":

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
    