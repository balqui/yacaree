"""
Project: yacaree

Current revision: mid Ventose 2025

Programmer: JLB

Little more than a str dunder for writing out (partial) implications.
Partial implications are made of two closures of type ItSet.
However, full implications have just a (frozen)set as antecedent and
one should not compute its support as we know it is the same as that
of the consequent.

Changed ItSet by Nivose 2025 so must follow up,
right now cannot have that easily the support of
rcn (rest of consequent), hence cannot compute 
easilly anything that depends on it.

CAVEAT: The current code still lacks the number of 
transactions dataset.nrtr needed to normalize supports.
"""

class Rule:

    def __init__(self, an, cn, full_impl = False):
        """
        They are to be ItSets, thus bring their supports with them,
        except when full_impl is True: then an can be a mere frozenset.
        """
        self.an = an
        self.cn = cn
        # ~ self.rcn = ItSet(cn.difference(an))
        self.rcn = cn.difference(an) # it is a set, we don't have its support
        self.supp = cn.supp # float(cn.supp) / latt.dataset.nrtr
        if full_impl:
            self.conf = 1
            self.connective = " ==> "
            self.s_s = -1
        else:
            self.conf = float(self.supp) / an.supp
            self.connective = " --> "
            self.s_s = float(cn.supp) / (an.supp - cn.supp)
        # ~ self.lift = ( float(self.suppboth) * latt.dataset.nrtr / (self.supprcn * self.suppant))
        # ~ self.levg = ( self.conf -
                      # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        # ~ self.p_s = ( self.supp -
                     # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        self.cboo = 0 # placeholder for the time being, MAYBE IT IS JUST AN UPPER BOUND but only if discarded
        self.lift = 0 # placeholder for the time being
        self.levg = 0 # placeholder for the time being


    def __str__(self):
        sp4 = "    "
        res = sp4 + " ".join(sorted(self.an)) # + "\n" + sp4 + sp4
        res += self.connective # + "\n" + sp4 + sp4 + sp4
        res += " ".join(sorted(self.rcn)) + " " # + "\n"
        res += ("[conf: %2.3f" % self.conf)
        res += ("; supp: %2d" % self.supp)
        # ~ res += ("supp: %2.3f; " % self.supp)
        # ~ res += ("lift: %2.3f; " % self.lift)
        # ~ res += ("leverage: %2.3f; " % self.levg)
        # ~ res += ("PS: %2.3f" % self.p_s)
        if self.s_s >= 0:
            res += ("; S-S: %2.3f" % self.s_s)
        if self.cboo == 0:
            res += "; ]\n"
        else:
            res += ("; boost: %2.3f]\n" % self.cboo)
        return res

if __name__ == "__main__":
    from itset import ItSet
    r1 = Rule(ItSet((str(e) for e in range(4)), 7), 
              ItSet((str(e) for e in range(7)), 5))
    print(r1)
    
