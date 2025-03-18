"""
yacaree

Current revision: mid / late Frimaire 2024 (but inffloat & removals after Pluviose 2025)

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

CAVEAT: Still to be heavily simplified as the refactoring reaches
the sophisticated algorithms.

Evolution of earlier module encompassing some static objects 
accessed from everywhere (or: Singleton pattern implemented 
as a module; spoiler: did not work well enough).

please_report - To report every now and then 

verbose: echo all log entries to terminal - UNCLEAR

scale: for writing ints as floats with controlled precision loss - UNCLEAR

epsilon: to compare floats to zero, try to avoid using it - TO BE REMOVED

pend_len_limit: limit on the size of the heap of closures pending for expansion - TO BE POSSIBLY REMOVED

pend_total_limit: max total length of info related to the pending closures - REMOVING IT

pend_mem_limit (was never actually implemented, TO BE REMOVED)

boostab: stability of boost, weight of current value in front of lift values coming in - TO STAY

confthr: was about 2/3 for long, scaled; set at 0.6 for somedays, not convincing, settling for 0.65 for v1.1
(natural alternatives to consider: 3/4 and 4/5) - TO STAY

supp_rep_often: how often to report about the ongoing support - CONCEPT CHANGED, CLARIFY

findrules: process bound, don't mine more than that many rules; if zero or negative, don't apply any bound - TO BE POSSIBLY REMOVED

maxrules: number of rules to be output, max boost among those found - TO STAY BUT CLARIFY

initialboost: initial bound on the confidence boost - TO STAY

absoluteboost: NO WAY any rule reported has lower boost than that, EVER - TO STAY

genabsupp: Do not consider closures with absolute support below this - TO STAY

"""

class HyperParam:

    def __init__(self):
        

        self.report_often = 2000 # report every that many closures
        self.check_size_often = 500 # test memory left every that many closures
        self.confthr = 0.65

        self.nrtr = 0  # to be updated by Dataset
        self.nrits = 0 # to be updated by Dataset

        self.pend_len_limit = 4098 # 8192 # 1000 # 16384 # 2 to power 14/13/12

        self.set_mode() # set to default

        # ~ self.tot_len_limit = 100000000 # requires often 4GB to 6GB core
                                       # but may end up eating 15GB
        # ~ self.tot_len_limit = 50000000 # half of above for testing 
        # ~ self.pend_total_limit = 100000000 # 100000 # 100000000
        # ~ self.pend_mem_limit = 1000000000 # 1GB

        # self.verbose = False
        # self.please_report = False # To report every now and then 
        # self.scale = 100000
        # self.epsilon = 100.0/self.scale
        # self.boostab = 5

        # ~ self.inffloat = float("inf") # infinite float, e.g. suppratios
        # ~ unclear whether worth it!

        ## standard process:
        
        ##confthr = int((2.0/3) * scale)
        # ~ self.confthr = int(0.65 * self.scale)
        # ~ self.findrules = 0
        # ~ self.maxrules = 50 # set this to zero if all the rules are to be written out
        # ~ self.stdmaxrules = self.maxrules # to recover the standard situation if necessary
        # ~ self.initialboost = 1.15
        # ~ self.absoluteboost = 1.05
        # ~ self.boostdecr = 0.001 # minimal boost decrease allowed

    def set_mode(self, mode = "stringent"):
        """
        Note: absolute number of transactions will be reduced to 3 if 
        dataset has less than 100 transactions.
        """
        if mode == "relaaaxed":
            self.genabsupp = 5 # absolute number of transactions
            self.abs_suppratio = 1.1 
            self.abs_m_impr = 1.1 

        if mode == "lenient":
            self.genabsupp = 10
            self.abs_suppratio = 1.15
            self.abs_m_impr = 1.15

        if mode == "stringent":
            "default"
            self.genabsupp = 1.2
            self.abs_suppratio = 1.2
            self.abs_m_impr = 15

        if mode == "harsh":
            self.genabsupp = 1.25 
            self.abs_suppratio = 1.25
            self.abs_m_impr = 25


