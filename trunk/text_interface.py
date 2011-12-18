from datetime import datetime

import statics

from iface import iface
from ruleminer import RuleMiner

if __name__ == "__main__":

##    fnm = "adultrain"
    fnm = "markbaskclem"
##    fnm = "pumsb_star"
##    fnm = "cmc-full"
##    fnm = "papersTr"
##    fnm = "votesTr"
##    next to be tested
##    fnm = "chess"
##    fnm = "connect"

    now = datetime.today().strftime("%Y%m%d%H%M%S")
    statics.logfile = iface.openfile(fnm + now + ".log","w")
    results_file = iface.openfile(fnm + now + "rules.txt","w")
    miner = RuleMiner(fnm)
    iface.endreport()
    rules = []
    for rul in miner.minerules():
##        iface.report(str(miner.count) + "/ " + str(rul))
        rules.append((-rul.cboo,rul))
        if miner.count == statics.maxrules > 0: break
    iface.report(str(miner.miner.card) +
                 " closures of support at least " +
                 str(miner.miner.minsupp) + ".")
    iface.report(str(miner.count) + " rules.")
    iface.endreport()
    cnt = 0
    for (b,r) in sorted(rules):
        cnt += 1
        results_file.write("\n" + str(cnt) + "/\n" + str(r))
    results_file.close()
    iface.report("Rules sorted according to confidence boost and written out; output file closed.")
    iface.report("End of process.")
    iface.endreport()
    if statics.logfile: statics.logfile.close()
    statics.logfile = None
## send ruleminer to garbage collector and recover free memory
    ruleminer = None
    exit(0)
