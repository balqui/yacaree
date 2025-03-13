"""
Project: yacaree

Current revision: late Ventose 2025

Programmer: JLB

Little more than a str dunder for writing out (partial) implications.
Partial implications are made of two closures of type ItSet.
However, full implications have just a (frozen)set as antecedent and
one should not compute its support as we know that it is the same as 
that of the consequent.

Changed ItSet by Nivose 2025 so must follow up,
right now cannot have that easily the support of
rcn (rest of consequent), hence cannot compute 
easily anything that depends on it.

CAVEAT: The current code still lacks the number of 
transactions dataset.nrtr needed to normalize supports.
"""

from math import isfinite
from iface import IFace

class Rule:

    def __init__(self, an, cn, full_impl = False):
        """
        They are to be ItSets, thus bring their supports with them,
        except when full_impl is True: then an can be a mere frozenset.
        """
        self.an = an
        self.cn = cn
        self.rcn = cn.difference(an) 
        # Careful: rcn is a set, not an ItSet,
        # because we don't have its support
        self.supp = cn.supp # float(cn.supp) / latt.dataset.nrtr
        if full_impl:
            self.conf = 1
            self.connective = " ==> "
            # ~ self.s_s = -1
        else:
            self.conf = float(self.supp) / an.supp
            self.connective = " --> "
            # ~ self.s_s = float(cn.supp) / (an.supp - cn.supp)

        self.m_impr = 0 # placeholder for mult improv for the time being
        # Careful: m_impr must be standard for full implications but
        # closure-aware for partial implications.
        self.cboo = 0
        self.sign = ''

    def set_cboo(self):
        if self.m_impr == 0:
            if not isfinite(self.cn.suppratio):
                IFace.reporterror("No confidence boost available " +
                    "for rule" + str(self))
            self.cboo = self.cn.suppratio
        elif self.m_impr < self.cn.suppratio:
            self.cboo = self.m_impr
            self.sign = "v"
        else:
            self.cboo = self.cn.suppratio
            self.sign = "^"


# ~ REMOVE ONE DAY:
        # ~ self.lift = 0 # placeholder for the time being
        # ~ self.levg = 0 # placeholder for the time being

        # ~ self.lift = ( float(self.suppboth) * latt.dataset.nrtr / (self.supprcn * self.suppant))
        # ~ self.levg = ( self.conf -
                      # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        # ~ self.p_s = ( self.supp -
                     # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        # ~ if not full_impl:
            # ~ print(" :: Made rule", self, "with conf", cn.supp, "/", an.supp)


    def __str__(self):
        sp4 = "    "
        res = sp4 + " ".join(sorted(self.an)) # + "\n" + sp4 + sp4
        res += self.connective # + "\n" + sp4 + sp4 + sp4
        res += " ".join(sorted(self.rcn)) + " " # + "\n"
        res += (f"[conf: {self.conf:5.3f}")
        res += (f"; supp: {self.supp:2d}") 
        res += (f" ({self.supp*100/IFace.hpar.nrtr:5.3f}%)")
        # ~ res += ("supp: %2.3f; " % self.supp) 
        # ~ res += ("lift: %2.3f; " % self.lift)
        # ~ res += ("leverage: %2.3f; " % self.levg)
        # ~ res += ("PS: %2.3f" % self.p_s)
        # ~ if self.s_s >= 0:
            # ~ res += ("; S-S: %2.3f" % self.s_s)
        if self.cboo == 0:
            res += "; ]"
        else:
            res += (f"; boost: {self.cboo:5.3f} ({self.sign})]")
        return res

if __name__ == "__main__":
    from itset import ItSet
    r1 = Rule(ItSet((str(e) for e in range(4)), 7), 
              ItSet((str(e) for e in range(7)), 5))
    print(r1)
    
