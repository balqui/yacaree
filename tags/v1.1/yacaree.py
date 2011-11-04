"""
Using yacaree through the GUI 
"""

from datetime import datetime

import statics
from ruleminer import RuleMiner
from choose_iface import iface

class Yacaree:

    def __init__(self):
        iface.go(self)

    def standard_run(self):
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        filenamenow = statics.filename + now
        filenamerules = filenamenow + "rules.txt"
        statics.logfile = iface.openfile(filenamenow + ".log","w")
        results_file = iface.openfile(filenamerules,"w")
        iface.disable_filepick()
        iface.disable_finish()
        iface.disable_run()
        miner = RuleMiner(statics.filenamefull) ## miner.miner is a ClMiner
        rules = []
        for rul in miner.minerules():
            rules.append((-rul.cboo,rul))
            if miner.count == statics.findrules > 0: break
        iface.report("Mining process terminated; searched for rules " + 
                     ("of confidence boost at least %1.3f." % miner.boosthr)) 
        iface.report(("Total of %d Rules obtained from " % miner.count) +
                     ("%d closures of support at least " % miner.miner.card) +
                     str(miner.miner.minsupp) + " (" +
                     str(miner.miner.to_percent(miner.miner.minsupp)) + "%).")
        cnt = 0
        for (b,r) in sorted(rules):
            cnt += 1
            results_file.write("\n" + str(cnt) + "/\n" + str(r))
            if cnt == statics.maxrules > 0: break
        results_file.close()
        iface.report("Confidence threshold was %2.3f."
                     % (float(statics.confthr)/statics.scale))
        iface.report(str(cnt) + " rules chosen according to their " +
                     "confidence boost written to file " + filenamerules + ".") 
        iface.report("End of process of dataset in file " + 
                     statics.filenamefull + ".")
        iface.report("Closing output and log files; run of yacaree " + 
                     statics.version + " finished.")
        statics.logfile.close()
        statics.logfile = None
        iface.enable_again()
        iface.enable_finish()
        iface.console.bell()

if __name__ == "__main__":

    y = Yacaree()
    

    
