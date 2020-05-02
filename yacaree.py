"""
Using yacaree through either the text CLI or the GUI. 
Current default is text CLI but this is likely to change.
"""

from datetime import datetime

import statics
from ruleminer import RuleMiner
##from choose_iface import iface

class Yacaree:

    def __init__(self):
        statics.iface.go(self)

    def standard_run(self):
        rulecnt = 0 # to avoid rule comparison in sorted(rules) at equal cboo
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        filenamenow = statics.filename + now
        filenamerules = filenamenow + "_rules.txt"
        statics.logfile = statics.iface.openfile(filenamenow + ".log","w")
        # ~ statics.iface.report() on log file, also must introduce itself there
        results_file = statics.iface.openfile(filenamerules,"w")
        statics.iface.disable_filepick()
        statics.iface.disable_finish()
        statics.iface.disable_run()
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
        statics.iface.enable_again()
        statics.iface.enable_finish()
        statics.iface.sound_bell()

    def standard_run_all(self):
        mmm = statics.maxrules 
        statics.maxrules = 0
        self.standard_run()
        statics.maxrules = mmm

if __name__ == "__main__":
    "The dataset will be changed later to a positional argument"
    
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = "Yet another closure-based association rule " +
                      "experimentation environment.",
        )
    argp.add_argument('-g', '--gui', action = 'store_true', help = "launch GUI")
    argp.add_argument('-v', '--version', action = 'version', 
                                         version = "%(prog)s " + statics.version)
    # ~ argp.add_argument('-d', '--dataset')
    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file")
    
    args = argp.parse_args()

    if args.gui:
        from iface import iface
    else:
        from iface_TEXT import iface
    
    statics.iface = iface
    
    if args.dataset:
        if args.gui:
            "GUI won't work as it has not been really set up yet, to be corrected"
            print("Sorry. In this version, using a GUI leads to forgetting the dataset. Load it again on the GUI please.")
        else:
            statics.iface.storefilename(args.dataset)

    y = Yacaree()

    
    

    
