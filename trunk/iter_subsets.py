"""
powerset iterators
"""

def all_subsets(aset):
    """
    iterator on powerset: all subsets of aset;
    if data is an iterator please call with set(iter)
    """
    if not aset:
        "empty"
        yield set([])
    else:
        e = aset.pop()
        for ss in all_subsets(aset):
            "each subset without e, and then with it"
            yield ss
            yield ss.union([e])
        aset.add(e) # reconstruct for the pending recursions

def all_proper_subsets(aset):
    if not aset:
        "empty: no proper subsets"
        pass
    elif len(aset) == 1:
        "empty subset only"
        yield set([])
    else:
        e = aset.pop()
        for ss in all_proper_subsets(aset):
            "each subset without e, and then with it"
            yield ss
            yield ss.union([e])
        yield aset # so far only its proper subsets went
        aset.add(e) # reconstruct


if __name__ == "__main__":
    t = set([0,1,2,3,4])
    for s in all_proper_subsets(t):
        print s



