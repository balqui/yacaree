"""
Using yacaree through the GUI
"""

from datetime import datetime

import statics
from ruleminer import RuleMiner
from iface import iface

class Yacaree:

    def __init__(self):
        iface.go(self)

    def standard_run(self):
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        filenamenow = statics.filename + now
        filenamerules = filenamenow + "rules.txt"
        statics.logfile = iface.openfile(filenamenow + ".log","w")
        results_file = iface.openfile(filenamerules,"w")
        iface.disable_finish()
        miner = RuleMiner(statics.filenamefull)
        rules = []
        for rul in miner.minerules():
            rules.append((-rul.cboo,rul))
            if miner.count == statics.findrules > 0: break
        iface.report(str(miner.count) + " rules obtained from " +
                     str(miner.miner.card) +
                     " closures of support at least " +
                     str(miner.miner.minsupp) + ".")
        cnt = 0
        for (b,r) in sorted(rules):
            cnt += 1
            results_file.write("\n" + str(cnt) + "/\n" + str(r))
            if cnt == statics.maxrules > 0: break
        results_file.close()
        iface.report(str(cnt) + " rules chosen and sorted according to their " +
                     "confidence boost written to file " + filenamerules + ".") 
        iface.report("End of process of dataset in file " + 
                     statics.filenamefull + ".")
        iface.report("Closing output and log files.")
        statics.logfile.close()
        statics.logfile = None
        iface.enable_again()
        iface.enable_finish()

if __name__ == "__main__":

    y = Yacaree()
    

    
