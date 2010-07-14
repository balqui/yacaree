from itset import ItSet

class Rule:

    def __init__(self,an,cn,latt):
        self.an = an
        self.cn = cn
        self.rcn = ItSet(cn.difference(an))
        self.supp = float(latt.supps[cn])/latt.dataset.nrtr
        self.conf = float(latt.supps[cn])/latt.supps[an]
        self.lift = (self.conf*latt.dataset.nrtr /
                     latt.supps[latt.close(self.rcn)])
        self.cboo = 0

    def __str__(self):
        res = ("[conf: %2.3f] " % self.conf)
        res += " ".join(sorted(self.an))
        res +=  " => "
        res += " ".join(sorted(self.rcn))
        res += (" [supp: %2.3f; " % self.supp)
        res += ("lift: %2.3f" % self.lift)
        if self.cboo == 0:
            res += "]"
        else:
            res += ("; conf boost: %2.3f] " % self.cboo)
        return res


            


