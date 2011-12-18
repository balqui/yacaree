"""
Project: Slatt
Package: hypergraph - taken almost verbatim from mid 2007 implementation
Programmers: JLB

Purpose: implement hypergraphs, mainly the minimal transversal operation

ToDo:
.testing when hyperedges are actually slanodes
.what happens when slanodes contain things beyond itemsets (trees, seqs...)
.more careful programming of transversal, avoiding duplicate exploration
.try algorithms A and B from Fredman-Khachiyan 
(now it is following blindly the basic strategy there)

"""

class hypergraph:
    """
    operations on hypergraphs: 
    each has a carrier (set of vertices) 
    and a list of hyperedges
    """

    def __init__(self, c=set([]), l = []):
        "initialization; default: empty carrier, empty list of hyperedges"
        self.carrier = c.copy()
        self.hyedges = [ e.copy() for e in l ]
        
    def addel(self,elem):
        "add one element to all the hyperedges"
        self.carrier.add(elem)
        for e in self.hyedges:
            e.add(elem)

    def added(self,ed=set([])):
        "add one hyperedge ed, empty by default - ed must be a set"
        for el in ed:
            self.carrier.add(el)
        self.hyedges.append(ed)

    def addhg(self,another):
        "union of two hypergraphs into the first one"
        for e in another.hyedges:
            self.added(e)

    def remel(self,elem):
        "remove element from all hyperedges where it belongs"
        for e in self.hyedges:
            if elem in e:
                e.remove(elem)

    def remed(self,elem):
        "remove all hyperedges where the element appears"
        new = []
        for e in self.hyedges:
            if not elem in e:
                new.append(e)
        del self.hyedges
        self.hyedges = new

    def _xcopy(self,thecopy):
        "copy hypergraph onto existing one"
        thecopy.carrier = self.carrier.copy()
        thecopy.hyedges = [e.copy() for e in self.hyedges]

    def copy(self):
        "make fresh copy of hypergraph"
        thecopy = hypergraph()
        thecopy.carrier = self.carrier.copy()
        thecopy.hyedges = [e.copy() for e in self.hyedges]
        return thecopy

    def updatecarrier(self):
        "after deleting hyperedges, remove elems possibly left over in carrier"
        new = set([])
        for e in self.hyedges:
            for el in e:
                new.add(el)
        self.carrier = new

    def somempty(self):
        "check for an empty hyperedge"
        for e in self.hyedges:
            if len(e)==0:
                return True
        return False

    def _newtransv(self,currtrs,newtr):
        """
        Find a new minimal transversal of self
        'new' means not covered by the current transversals currtrs
        currtrs must consist initially only of transversals of self
        returns True if a new transversal found in newtr
        returns False if no new transversals exist: currtrs is the tr h of self
        """

        self.updatecarrier()
        
        if len(self.hyedges)==0:
            if currtrs.somempty():
                return False
            else:
                newtr = set([])
                return True
        elif self.somempty():
            return False
        else:
            selflocal = hypergraph()
            currlocal = hypergraph()
            for el in self.carrier:
                "try el not in newtr"
                self._xcopy(selflocal)
                currtrs._xcopy(currlocal)
                selflocal.remel(el)
                currlocal.remed(el)
                if selflocal._newtransv(currlocal,newtr):
                    return True
                else:
                    "try el in newtr"
                    self._xcopy(selflocal)
                    currtrs._xcopy(currlocal)
                    selflocal.remed(el)
                    currlocal.remel(el)
                    fd = selflocal._newtransv(currlocal,newtr)
                    if fd:
                        newtr.add(el)
                        return True
                    else:
                        return False

    def transv(self):
        """
        Find the hypergraph of minimal transversals of self
        """
        currtrs = hypergraph()
        newtr = set([])
        while self._newtransv(currtrs,newtr):
            currtrs.added(newtr.copy())
            newtr = set([])
        return currtrs

    def simplify(self):
        """
        Obtain a simple hypergraph by removing nonminimal hyperedges
        But does not remove duplicates
        Careful: one of the calls might assume no reordering
        """
        sieve = self.hyedges
        for e in self.hyedges:
            sieve = [ e1 for e1 in sieve if not e<e1 ]
        self.hyedges = sieve

    def rmdups(self):
        "remove duplicate edges - sometimes they creep in"
        nodups = []
        for e in self.hyedges:
            if not e in nodups:
                nodups.append(e)
        self.hyedges = nodups

if __name__ == "__main__":
    print "slatt module hypergraph called as main and running as test"

    h = hypergraph()

#    small tests

    h.added(set(['A']))
    h.added(set(['B']))

    h.added(set(['A','B']))
    h.added(set(['B','C']))
    h.added(set(['B','D']))
    h.added(set(['C','D']))

    h.added(set(['A','B','C']))
    h.added(set(['B','C','D']))

    print "h has 8 hyedges on A, B, C, D"
    print h.carrier
    print h.hyedges

# must add testing for addhg etc

    hh = h.copy()
##    hhh = hypergraph()
##    h.xcopy(hhh)

    h.added(set(['A','D']))

    h.simplify()
#    h.simplify({'A':['B','C']})

    print "h modified: added AD and simplified:"
    print h.carrier
    print h.hyedges

    print "hh, a copy of h before modification:"
    print hh.carrier
    print hh.hyedges

##    print "hhh, an xcopy of h before modification:"
##    print hhh.carrier
##    print hhh.hyedges


    t = hypergraph()
    t = h.transv()

    print "h again:"
    print h.carrier
    print h.hyedges
    print "t, its transversal:"
    print t.carrier
    print t.hyedges

    h = hypergraph(set(['1','2']),[set('1'),set('2')])

    print "fully changed h"
    print h.carrier
    print h.hyedges

    print "did t change as well?"
    print t.carrier
    print t.hyedges

    t = hypergraph()
    t = h.transv()

    print "initialized h and its transversal"
    print h.carrier
    print h.hyedges
    print t.carrier
    print t.hyedges

    print "another hypergraph hh on different universe"
    hh = hypergraph(set(['1','2','3']),[set(['1','2']),set(['2','3'])])
    print hh.carrier
    print hh.hyedges


