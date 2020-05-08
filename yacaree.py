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
        statics.iface.report_log_file(filenamenow)
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
        statics.maxrules = statics.stdmaxrules # Just in case something was recently tweaked
        statics.iface.sound_bell()

    def standard_run_all(self):
        "needed as a single button command - std run will get back on its own the std figure afterwards"
        statics.maxrules = 0
        self.standard_run()

if __name__ == "__main__":
    "The dataset will be changed later to a positional argument"
    
    from argparse import ArgumentParser
    argp = ArgumentParser(
        description = "Yet another closure-based association rule " +
                      "experimentation environment.",
        prog = "python[2|3] yacaree.py"
        )

    argp.add_argument('-a', '--all', action = 'store_true', 
                      help = "output with no rule limit (default: limit to " 
                           + str(statics.maxrules) + " rules)")
    argp.add_argument('-g', '--gui', action = 'store_true', 
                      help = "launch GUI (default: remain in command line interface - CLI)")
    argp.add_argument('-v', '--version', action = 'version', 
                                         version = "yacaree " + statics.version,
                                         help = "print version and exit")
    argp.add_argument('-t', '--test', action = 'store_true')
    # ~ argp.add_argument('-d', '--dataset') # Not anymore an option but a positional argument
    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file (default: none, ask user)")
    
    args = argp.parse_args()

    if args.all:
        statics.maxrules = 0

    if args.test and args.gui:
        from iface_TEXT_aux import iface_gui as iface
    elif args.gui:
        "no test"
        from iface import iface
    elif args.test:
        "no gui"
        from iface_TEXT_aux import iface_text as iface
    else:
        "no test, no gui"
        from iface_TEXT import iface
    
    if args.test:
        statics.iface = iface()
    else:
        statics.iface = iface
    
    if args.dataset:
        statics.iface.storefilename(args.dataset)

    y = Yacaree()

    
    

    
