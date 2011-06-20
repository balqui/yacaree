
##    def pend_clos_size(self,pend_clos):
##        "by memory size, should try to spare recomputing it so often"
##        m = sys.getsizeof(pend_clos)
##        for b in pend_clos:
##            m += (sys.getsizeof(b[0]) +
##                  sys.getsizeof(b[1]) +
##                  sys.getsizeof(b[2]))
##        return m

##    def pend_clos_size(self):
##        "by lengths, insufficient for dense or big datasets"
##        m = len(self.pend_clos)
##        for pend in self.pend_clos:
##            m += len(pend[1]) + len(pend[2])
##        return m

##    def halve_pend_clos(self):
##        """
##        too many closures pending expansion: raise
##        the support bound so that about half of the
##        pend_clos heap becomes discarded
##        """
##        lim = self.cnt_pend / 2
##        current_supp = self.dataset.nrtr + 1
##        current_supp_clos = []
##        new_pend_clos = []
##        new_cnt = 0
##        old_intsupp = self.intsupp
##        while self.pend_clos:
##            b = heappop(self.pend_clos)
##            new_cnt += 1
##            if new_cnt > lim: break
##            if -b[0] == current_supp:
##                current_supp_clos.append(b)
##            else:
##                self.intsupp = current_supp
##                current_supp = -b[0]
##                new_pend_clos.extend(current_supp_clos)
##                current_supp_clos = [b]
##        self.pend_clos = new_pend_clos
##        iface.report("Increased min support from " + str(old_intsupp) +
##                     (" (%2.3f%%) up to " % self.to_percent(old_intsupp)) + 
##                     str(self.intsupp) +
##                     (" (%2.3f%%)" % self.to_percent(self.intsupp)) + ".")
        
