#! /usr/bin/env python3

"""
yacaree

Current revision: late Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Using yacaree through either the text CLI or the GUI on *nix.
Current default is text CLI but this might change.

Heavily refactored from the 1.* versions: hyperparameters and
interface replaced the early statics.py now not anymore used.

Must change the report messages in terms of f-strings.

Should review the -a option and clarify the labels on the buttons.

"""

from iface import IFace
from hyperparam import HyperParam
from dataset import Dataset
from ruleminer import RuleMiner

class Yacaree:

    def __init__(self, iface, hpar, datafilename):
        self.hpar = hpar
        self.iface = iface
        self.dataset = None
        self.datafilename = datafilename
        self.iface.go(self)

    def standard_run(self):
        if self.hpar.maxrules == 0:
            self.iface.report("CLI call requested all rules as output.")
        if not self.dataset:
            self.dataset = Dataset() # reads in from iface.datafile
        self.iface.openauxfiles()

        rulecnt = 0 # avoid comparing rules of same cb in sorted(rules) 
        results_file = self.iface.rulesfile
        self.iface.get_ready_for_run()
        if self.hpar.maxrules == 0:
            self.iface.report("Providing all rules as output.")
        self.iface.running = True
        miner = RuleMiner(self.iface, self.hpar, self.dataset) # ClMiner
        rules = []
        for rul in miner.minerules():
            "if someday Rule has comparison, remove mentions to rulecnt"
            rulecnt += 1
            rules.append((-rul.cboo, rulecnt, rul))
            if miner.count == self.hpar.findrules > 0: break
        self.iface.report("Mining process terminated;" + 
                          " searched for rules of confidence boost" + 
                         (" at least %1.3f." % miner.latt.boosthr)) 
        self.iface.report(("Total of %d Rules obtained from " % miner.count) +
                     ("%d closures of support at least " % miner.latt.miner.card) +
                     str(miner.latt.miner.minsupp) + " (" +
                     str(miner.latt.miner.to_percent(miner.latt.miner.minsupp)) + "%).")
        cnt = 0
        for (b, c, r) in sorted(rules):
            "remove c in case rulecnt is removed"
            cnt += 1
            results_file.write("\n" + str(cnt) + "/\n" + str(r))
            if cnt == self.hpar.maxrules > 0: break
        results_file.close()
        self.iface.report("Confidence threshold was %2.3f."
                     % (float(self.hpar.confthr)/self.hpar.scale))
        self.iface.report(str(cnt) + " rules chosen according to their " +
                     "confidence boost written to file " + self.iface.rulesfile.name + ".") 
        self.iface.report("End of process of dataset in file " + 
                     self.iface.datafile.name + ".")
        self.iface.report("Closing output and log files; run of yacaree " + 
                     self.iface.version + " finished.")
        self.iface.logfile.close()
        self.iface.get_ready_for_new_run()
        self.hpar.maxrules = self.hpar.stdmaxrules # Just in case something was recently tweaked
        self.iface.sound_bell()

    def standard_run_all(self):
        "needed as a single button command - std run will get back on its own the std figure afterwards ?????"
        self.hpar.maxrules = 0
        self.standard_run()

if __name__ == "__main__":
    
    from argparse import ArgumentParser

    iface = IFace()
    hpar = HyperParam()

    argp = ArgumentParser(
        description = "Yet another closure-based association rule " +
                      "experimentation environment (CLI *nix flavor, " +
                      "alt Win/*nix-compatible double-click launch " +
                      "in file yacaree.pyw).",
        prog = "python[3] yacaree.py or just ./yacaree"
        )

    argp.add_argument('-a', '--all', action = 'store_true', 
                      help = "output with no rule limit " + 
                             "(default: limit to " 
                             + str(hpar.maxrules) + " rules)")
    argp.add_argument('-g', '--gui', action = 'store_true', 
                      help = "launch GUI (default: remain in " + 
                             "command line interface - CLI)")
    argp.add_argument('-v', '--verbose', action = 'store_true', 
                      help = "verbose report of current support " + 
                             "at every closure")
    argp.add_argument('-V', '--version', action = 'version', 
                            version = "yacaree " + iface.version,
                            help = "print version and exit")
    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file " + 
                             "(default: none, ask user)")
    
    # ~ argp.add_argument('-t', '--test', action = 'store_true') 
    # ~ # for testing times (???)

    args = argp.parse_args()

    if args.all:
        hpar.maxrules = 0

    if args.verbose:
        hpar.verbose = True

    iface.gui = args.gui

    y = Yacaree(iface, hpar, args.dataset)

