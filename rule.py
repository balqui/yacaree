"""
Nivose 2025: changed ItSet so must follow up,
right now cannot create rcn (rest of consequent)
as I will not have its support that easily,
hence cannot compute anything that depends on
the support of rcn.

CAVEAT: The current code still lacks the number of 
transactions dataset.nrtr needed to normalize supports
"""

class Rule:

    def __init__(self, an, cn):
        """
        They are ItSets, thus bring their supports with them.
        """
        self.an = an
        self.cn = cn
        # ~ self.rcn = ItSet(cn.difference(an))
        self.rcn = cn.difference(an) # it is a set, we don't have its support
        self.supp = float(cn.supp) # / latt.dataset.nrtr
        self.conf = float(self.supp) / an.supp
        # ~ self.lift = ( float(self.suppboth) * latt.dataset.nrtr / (self.supprcn * self.suppant))
        # ~ self.levg = ( self.conf -
                      # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        # ~ self.p_s = ( self.supp -
                     # ~ float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        if an.supp - cn.supp > 0:
            self.s_s = float(cn.supp) / (an.supp - cn.supp)
        else:
            self.s_s = -1
        self.cboo = 0

    def __str__(self):
        sp4 = "    "
        res = sp4 + " ".join(sorted(self.an))
        res +=  "\n" + sp4 + sp4 + "=> \n" + sp4 + sp4 + sp4
        res += " ".join(sorted(self.rcn))
        res += ("\n[conf: %2.3f; " % self.conf)
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
    
