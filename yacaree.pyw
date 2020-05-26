#!/usr/bin/env python3

"""
Attempt at using GUI-based yacaree on Windows by just
double-click through the Python Launcher for Windows. 
"""

from datetime import datetime

import statics
from ruleminer import RuleMiner

class Yacaree:

    def __init__(self):
        statics.iface.go(self)

    def standard_run(self):
        rulecnt = 0 # to avoid rule comparison in sorted(rules) at equal cboo
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        filenamenow = statics.filename + now
        filenamerules = filenamenow + "_rules.txt"
        statics.logfile = statics.iface.openfile(filenamenow + ".log","w")
        statics.iface.report_log_file(filenamenow)
        results_file = statics.iface.openfile(filenamerules,"w")
        statics.iface.get_ready_for_run()
        if statics.maxrules == 0:
            statics.iface.report("Providing all rules as output.")
        miner = RuleMiner(statics.filenamefull) ## miner.miner is a ClMiner
        rules = []
        for rul in miner.minerules():
            "if someday Rule has comparison, remove all mentions to rulecnt"
            rulecnt += 1
            rules.append((-rul.cboo, rulecnt, rul))
            if miner.count == statics.findrules > 0: break
        statics.iface.report("Mining process terminated; searched for rules " + 
                     ("of confidence boost at least %1.3f." % miner.latt.boosthr)) 
        statics.iface.report(("Total of %d Rules obtained from " % miner.count) +
                     ("%d closures of support at least " % miner.latt.miner.card) +
                     str(miner.latt.miner.minsupp) + " (" +
                     str(miner.latt.miner.to_percent(miner.latt.miner.minsupp)) + "%).")
        cnt = 0
        for (b, c, r) in sorted(rules):
            "remove c in case rulecnt is removed"
            cnt += 1
            results_file.write("\n" + str(cnt) + "/\n" + str(r))
            if cnt == statics.maxrules > 0: break
        results_file.close()
        statics.iface.report("Confidence threshold was %2.3f."
                     % (float(statics.confthr)/statics.scale))
        statics.iface.report(str(cnt) + " rules chosen according to their " +
                     "confidence boost written to file " + filenamerules + ".") 
        statics.iface.report("End of process of dataset in file " + 
                     statics.filenamefull + ".")
        statics.iface.report("Closing output and log files; run of yacaree " + 
                     statics.version + " finished.")
        statics.logfile.close()
        statics.logfile = None
        statics.iface.get_ready_for_new_run()
        statics.maxrules = statics.stdmaxrules # Just in case something was recently tweaked
        statics.iface.sound_bell()

    def standard_run_all(self):
        "needed as a single button command - std run will get back on its own the std figure afterwards"
        statics.maxrules = 0
        self.standard_run()

if __name__ == "__main__":
    
    from iface import iface_gui as iface
    
    statics.iface = iface()

    y = Yacaree()

    
    

    
