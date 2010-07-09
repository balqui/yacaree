"""
Programmers: JLB

Purpose: implementing lattice nodes and other itemset usages such as generators

Inherits from frozenset so that they can index dictionaries

Offers:
.supp, card, setsupp()
..this last op needed because I cannot manage to inform it upon __init__()
.placeholders 
..mxs (max supp of a subset)
..mns (min supp of a superset)
..gmxs (max supp of a minimal generator that reaches some conf thr to the node)
.revise() to change the contents of the slanode while preserving the mxs/mns values - returns a new slanode
.package contributes ops outside class:
..set2node to make a slanode from an iterable like set or frozenset
..str2node to make a slanode by parsing a line like the Borgelt output
.auxitset(string-or-another-iterable), auxiliary class to parse into set and support
..then coerce into slanode the auxitset and call setsupp(supp)

Notes:
.supp is an integer, absolute support; dataset size needed to compute relative support
.may want to use customized separator character to read the support from the apriori output ('/' or ';' or...)

ToDo:
.try Python 3.0 to inform the support upon __init__() and simplify (could then remove auxitset, set2node, str2node)
.add initialization for output from other closure miners such as Zaki's RULES
.some day the contents should be able to accommodate trees and sequences and...
"""

class auxitset(set):
    "it is a set via inheritance, and additionally has supp(ort)"
    def __init__(self,contents=[],supp=0):
        """
        parse out set from contents, either a set or a string ---
        the string might contain support info as with Borgelt apriori -a output
        """
        if isinstance(contents,str):
            sepsupp = contents.split('/')
            cont = sepsupp[0].strip('( ').split()
            if len(sepsupp)>1:
                "comes with support info"
                supp = int(sepsupp[1].strip(')%\n\r'))
        else:
            "must be an iterable"
            cont = contents
        set.__init__(set([]))
        for el in cont:
            self.add(el)
        self.supp = supp

def str2node(string=""):
    st1 = auxitset(string)
    st2 = slanode(st1)
    st2.setsupp(st1.supp)
    return st2

def set2node(st=set([]),spp=0):
    st2 = slanode(st)
    st2.setsupp(spp)
    return st2

class slanode(frozenset):
    """
    Tried hard to have a single class by initializing from string, list or set
    directly within the __init__ of itset - never worked, and never understood
    the error messages. At least this workaround works indeed around...
    """

    def __init__(self,contents):
        frozenset.__init__(contents)
        self.supp = 0
        self.card = len(contents)
        self.mxs = -1
        self.mns = -1
        self.gmxs = -1

    def setsupp(self,supp):
        self.supp = supp

    def __str__(self,trad={}):
        """
        prettyprint of itemset: support omitted if zero
        optional element translator trad
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
        if self.supp > 0:
            s = s + " (" + str(self.supp) + ")"
        return s

    def copy(self):
        ss = slanode(self)
        ss.setsupp(self.supp)
        ss.mxs = self.mxs
        ss.gmxs = self.gmxs
        ss.mns = self.mns
        return ss

    def revise(self,c):
        ss = slanode(c)
        ss.setsupp(self.supp)
        ss.mxs = self.mxs
        ss.gmxs = self.gmxs
        ss.mns = self.mns
        return ss


if __name__=="__main__":
    "some little testing needed here"
    pass

##    print "slatt module itset called as main and running as test..."

