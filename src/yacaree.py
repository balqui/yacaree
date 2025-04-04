#! /usr/bin/env python3

"""
yacaree

Current revision: late Ventose 2025, only CLI for today

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Using yacaree through either the text CLI or the GUI on *nix.
Current default is text CLI but this might change.

Heavily refactored from the 1.* versions: hyperparameters and
interface replaced the early statics.py now not anymore used.

CAVEAT: Must change the report messages in terms of f-strings.

CAVEAT: Should review the -a option, right now it reports all 
the rules, not sure whether I want back the option of limiting 
then to 50.

CAVEAT: Should review the -v option, right now it is as verbose
as I want it.

CAVEAT: Clarify the labels on the buttons.
"""

from iface import IFace
from hyperparam import HyperParam
from dataset import Dataset
from ruleminer import RuleMiner

class Yacaree:

    def __init__(self, hpar, datafilename):
        from operator import attrgetter
        self.hpar = hpar
        self.dataset = None
        self.datafilename = datafilename
        self.cboo_f = attrgetter('cboo') # extract cboo from rules
        # ~ self.iface.go(self) # moved off

    def standard_run(self):
        # ~ if self.hpar.maxrules == 0:
            # ~ self.iface.report("CLI call requested all rules as output.")

        if not self.dataset:
            self.dataset = Dataset() # reads in from iface.datafile
        IFace.openauxfiles()

        rulecnt = 0 # avoid comparing rules of same cb in sorted(rules) CAVEAT: I BELIEVE THIS UNNECESSARY NOW (???)
        IFace.get_ready_for_run()
        # ~ if self.hpar.maxrules == 0:
            # ~ self.iface.report("Providing all rules as output.")

        self.hpar.set_mode(iface.mode) # iface from main, version needs it there

        iface.running = True # iface from main

        miner = RuleMiner(self.hpar, self.dataset)
        rules = []
        for rul in miner.minerules():
            rulecnt += 1
            rules.append(rul)
        IFace.report("Mining process terminated; searched for" + 
                " rules of confidence boost "
                f"{min(hpar.abs_suppratio, hpar.abs_m_impr):4.2f}.")
        IFace.report(("Total of %d Rules obtained from " % miner.count) +
                     ("%d closures of support at least " % len(miner.latt)) +
                     str(miner.latt.minsupp))
                      # ~ + " (" +
                     # ~ str(miner.latt.miner.to_percent(miner.latt.miner.minsupp)) + "%).")
        cnt = 0
        for r in sorted(rules, reverse = True, key = self.cboo_f):
            cnt += 1
            IFace.rulesfile.write("\n" + str(cnt) + "/ " + str(r))
            # ~ if cnt == self.hpar.maxrules > 0: break
        IFace.rulesfile.close()
        IFace.report(f"Confidence threshold was {self.hpar.confthr:4.2f}.")
        IFace.report(str(cnt) + " rules chosen according to their " +
                     "confidence boost written to file " + IFace.rulesfile.name + ".") 
        IFace.report("End of process of dataset in file " + 
                     IFace.datafile.name + ".")
        IFace.report("Closing output and log files; run of yacaree " + 
                     IFace.version + " finished.")
        IFace.logfile.close()
        IFace.get_ready_for_new_run()
        # ~ self.hpar.maxrules = self.hpar.stdmaxrules # Just in case something was recently tweaked
        IFace.sound_bell()

    # ~ def standard_run_all(self): # PLANNING TO REMOVE THIS OPTION
        # ~ "needed as a single button command - std run will get back on its own the std figure afterwards ?????"
        # ~ self.hpar.maxrules = 0
        # ~ self.standard_run()

if __name__ == "__main__":

    from filenames import FileNames
    from argparse import ArgumentParser

    iface = IFace()
    hpar = HyperParam()

    argp = ArgumentParser(
        description = "Yet another closure-based association rule " +
                      "experimentation environment.",
                      # ~ "experimentation environment (CLI *nix flavor, " +
                      # ~ "alt Win/*nix-compatible double-click launch " +
                      # ~ "in file yacaree.pyw).",
        # ~ prog = "python[3] yacaree.py or just ./yacaree"
        prog = "./yacaree"
        )

    argp.add_argument('-g', '--gui', action = 'store_true', 
                      help = "launch GUI (default: remain in " + 
                             "command line interface - CLI)")
    argp.add_argument('-V', '--version', action = 'version', 
                            version = "yacaree " + IFace.version,
                            help = "print version and exit")
    argp.add_argument('dataset', nargs = '?', default = None, 
                      help = "name of optional dataset file " + 
                             "(default: none, ask user)")

    argp.add_argument('-m', '--mode', 
            choices = ['harsh', 'stringent', 'lenient', 'relaaaxed'], 
            default = 'stringent',
            help = "how strict are we to be")

    args = argp.parse_args()

    iface.gui = args.gui

    y = Yacaree(hpar, args.dataset)
    IFace.go(y, args.mode)

# ~ DOUBTFUL FLAGS:

    # ~ argp.add_argument('-t', '--test', action = 'store_true') 
    # ~ # for testing times (???)

    # ~ argp.add_argument('-a', '--all', action = 'store_true', 
                      # ~ help = "output with no rule limit " + 
                             # ~ "(default: limit to " 
                             # ~ + str(hpar.maxrules) + " rules)")
    # ~ argp.add_argument('-v', '--verbose', action = 'store_true', 
                      # ~ help = "verbose report of current support " + 
                             # ~ "at every closure")

    # ~ if args.all:
        # ~ hpar.maxrules = 0

    # ~ if args.verbose:
        # ~ hpar.verbose = True

# ~ EARLIER TEST CODE:

    # ~ from time import time

    # ~ fnm = "../data/lenses_recoded"
    # ~ fnm = "../data/toy"
    # ~ fnm = "../data/e24.td"
    # ~ fnm = "../data/e24t.td"
    # ~ fnm = "../data/e13"
    # ~ fnm = "../data/e13a"
    # ~ fnm = "../data/e13b"
    # ~ fnm = "../data/adultrain"
    # ~ fnm = "../data/cmc-full"
    # ~ fnm = "../data/papersTr" # FILLS MEMORY ANYHOW EVEN WITH THE TOTAL SUPPORT SET LENGTHS LIMIT
    # ~ fnm = "../data/votesTr" 
    # The next work thanks to the limit on the total support set lengths
    # ~ fnm = "../data/chess.td"   # Fills memory with small heap size
    # ~ fnm = "../data/connect.td" # Fills memory with ridiculous heap
                                   # size and less than 5000 closures

    # ~ iface = IFace()
    # ~ hpar = HyperParam()

    # ~ IFace.fn = FileNames(IFace)
    # ~ IFace.opendatafile(fnm)
    # ~ d = Dataset()

    # ~ y = Yacaree(iface, hpar, fnm)

    # ~ miner = ClMiner(d, 0.084)
    # ~ miner = ClMiner(d, 0.75)
    # ~ miner = ClMiner(d, 3/24)
    # ~ miner = ClMiner(d, 0)
    # ~ print("Int support:", miner.intsupp)
    # ~ lcl = list()
    # ~ for cl in miner.mine_closures():
        # ~ lcl.append(cl)
        # ~ if miner.card > IFace.hpar.clos_num_limit:
            # ~ break
        # ~ print(cl)
    # ~ print(f"Number of closures: {len(lcl)} of " + 
          # ~ f"support {cl.supp} of more; total lengths {miner.totlen}.") # or miner.card
    # ~ print("In dict:")
    # ~ for fs in miner:
        # ~ if miner[fs].supp == 0:
            # ~ print(fs, miner[fs])

