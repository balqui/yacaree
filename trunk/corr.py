"""
Project: Slatt
Package: corr
Creation: november 25th, 2008, and thoroughly revised afterwards
Programmers: JLB

Purpose: 
.implement correspondence tightening
..(auxiliary process for rule mining)

Inherits from dict:
.it is a dict of lists
.the dict keys must admit a comparison operation (partial order)
.adds the operation of tightening: each element in a list remains only
 in those lists corresponding to keys that are maximal among those
 keys of lists where the element appears

ToDo:
.try to find better algorithmics
"""

class corr(dict):

    def __init__(self):
        dict.__init__(self)

    def tighten(self,progcnt=None):
        "may use a verbosity object progcnt to report progress"
        ticking = (progcnt!=None)
        for e in self.keys():
            if ticking:
                progcnt.tick()
            valids = []
            for g in self[e]:
                for ee in self.keys():
                    if e < ee and g in self[ee]:
                        break
                else:
                    valids.append(g)
            self[e] = valids

if __name__=="__main__":

    print "slatt module corr called as main and running as test..."

    c = corr()

    for i in range(10):
        c[i] = []
        for k in range(6):
            c[i].append(str(i+3*k))

    print "==="

    print c

    for e in c.keys():
        print e, ":", c[e]

    print "==="

    c.tighten()

    print "==="

    print c

    for e in c.keys():
        print e, ":", c[e]

    print "==="




