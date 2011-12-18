""" careful:
adding leverage, does not belong to 1.0, maybe 1.1
also adding one space at the support
to do: remove from self the local supps
"""

from itset import ItSet

class Rule:

    def __init__(self,an,cn,latt):
        self.an = an
        self.cn = cn
        self.rcn = ItSet(cn.difference(an))
        self.suppboth = latt.supps[cn]
        self.suppant = latt.supps[an]
        self.supprcn = latt.supps[latt.close(self.rcn)]
        self.supp = float(self.suppboth) / latt.dataset.nrtr
        self.conf = float(self.suppboth) / self.suppant
        self.lift = ( float(self.suppboth) * latt.dataset.nrtr / (self.supprcn * self.suppant))
        self.levg = ( self.conf -
                      float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        self.p_s = ( self.supp -
                     float(self.supprcn*self.suppant)/(latt.dataset.nrtr*latt.dataset.nrtr) )
        if self.suppant - self.suppboth > 0:
            self.s_s = float(self.suppboth) / (self.suppant - self.suppboth)
        else:
            self.s_s = -1
        self.cboo = 0

    def __str__(self):
        sp4 = "    "
        res = sp4 + " ".join(sorted(self.an))
        res +=  "\n" + sp4 + sp4 + "=> \n" + sp4 + sp4 + sp4
        res += " ".join(sorted(self.rcn))
        res += ("\n[conf: %2.3f; " % self.conf)
        res += ("supp: %2.3f; " % self.supp)
        res += ("lift: %2.3f; " % self.lift)
##		res += ("suppboth: %d; " % self.suppboth)
##		res += ("suppant: %d; " % self.suppant)
##		res += ("supprcn: %d; " % self.supprcn)
        res += ("leverage: %2.3f; " % self.levg)
        res += ("PS: %2.3f" % self.p_s)
        if self.s_s >= 0:
            res += ("; S-S: %2.3f" % self.s_s)
        if self.cboo == 0:
            res += "; ]\n"
        else:
            res += ("; boost: %2.3f]\n" % self.cboo)
        return res


##    def __str__(self):
##        res = ("[conf: %2.3f] " % self.conf)
##        res += " ".join(sorted(self.an))
##        res +=  " => "
##        res += " ".join(sorted(self.rcn))
##        res += (" [supp: %2.3f; " % self.supp)
##        res += ("lift: %2.3f" % self.lift)
##        if self.cboo == 0:
##            res += "]"
##        else:
##            res += ("; conf boost: %2.3f] " % self.cboo)
##        return res


            


