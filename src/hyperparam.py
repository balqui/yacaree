"""
yacaree

Current revision: mid / late Frimaire 2024 (but inffloat & removals after Pluviose 2025)

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Heavily simplified as the refactoring reaches the sophisticated algorithms.

CAVEAT: Still requires some work.

Current quandary: mode in hpar is a Python string, mode in IFace 
is a Tk StringVar(), and they have to be in lockstep: change is
effected in IFace but consequences are to be guided from hpar.

I see two options: a/ manage to bind hpar.mode to the radio buttons, 
but for this I need it to be a Tk StringVar, whose creation requires
previous existence of a Tk() which is created in IFace.go() which also
launches the run: too late for setting up the mode; b/ import somehow 
the IFace field inside hpar but unclear then how to entangle them.

Evolution of earlier module encompassing some static objects 
accessed from everywhere (or: Singleton pattern implemented 
as a module; spoiler: did not work well enough).

verbose: echo all log entries to terminal - UNCLEAR

confthr: was about 2/3 for long, scaled; set at 0.6 for somedays, not convincing, settling for 0.65 for v1.1
(natural alternatives to consider: 3/4 and 4/5) - TO STAY

maxrules: number of rules to be output, max boost among those found - DOUBTFUL, NOT IMPLEMENTED CURRENTLY

genabsupp: Do not consider closures with absolute support below this - TO STAY

"""

# ~ from iface import IFace # only necessary for the mode property

class HyperParam:

    def __init__(self):
        
        self.report_often = 2000 # report every that many closures
        self.check_size_often = 500 # test memory left every...
        self.confthr = 0.65

        self.nrtr = 0  # to be updated by Dataset
        self.nrits = 0 # to be updated by Dataset

        self.pend_len_limit = 4098 # 2 to power 12
        # Alternatives considered: 1000, 8192, 16384 = 2 to power 14

    def set_mode(self, mode):
        """
        Note: absolute number of transactions will be reduced to 3 if 
        dataset has less than 100 transactions.
        """
        # ~ print(" ---- in set_mode", mode, self.nrtr)

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
            self.genabsupp = 15
            self.abs_suppratio = 1.2
            self.abs_m_impr = 1.2

        if mode == "harsh":
            self.genabsupp = 25 
            self.abs_suppratio = 1.25
            self.abs_m_impr = 1.25

        if self.nrtr < 100:
            # ~ print(" .. support down to 3")
            self.genabsupp = 3


# ~ DEPRECATED FIELDS:
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
