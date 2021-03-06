"""

Project: yacaree
Programmer: JLB

Description:

transactional dataset, read in from a txt file
one transaction per line
items in each transaction separated by whitespace
 as per string method split()
whitespace characters as per split() cannot occur
 inside the items
empty transactions are ignored
dataset replicated into two dicts:
 transcns: set of items per transaction id (unsigned, starts at zero)
 occurncs: set of transaction ids per item
also:
 scale (maybe to migrate somewhere else)
 nrits
 nrtr
 nrocc
 univ
 dataset filename
 datasetfile, closed, should one need to open it again

"""

from collections import defaultdict

import statics

class Dataset:

    def __init__(self,filename=None):
        "find actual file, open, and read the dataset in - redundancies left"
        self.datasetfile = statics.iface.openfile(statics.filenamefull)
        statics.iface.report("Reading in dataset from file " +
                     statics.filenamefull)
        self.nrocc = 0
        self.nrtr = 0
        self.univ = set()
        self.transcns = defaultdict(set)
        self.occurncs = defaultdict(set)
        for line in self.datasetfile:
            isempty = True
            for el in line.strip().split():
                if len(el)>0:
                    isempty = False
                    self.nrocc += 1
                    self.univ.add(el)
                    self.transcns[self.nrtr].add(el)
                    self.occurncs[el].add(self.nrtr)
            if not isempty:
                self.nrtr += 1
        self.nrits = len(self.univ)
        self.datasetfile.close()
        statics.iface.report("Dataset read in. Consists of " +
                     str(self.nrtr) + " transactions from among " +
                     str(self.nrits) + " different items, with a total of " +
                     str(self.nrocc) + " item occurrences.")

    def inters(self,lstr):
        "for an iterable of transactions lstr, return their intersection"
        items = self.univ.copy()
        for t in lstr:
            items &= self.transcns[t]
        return items

if __name__ == "__main__":

    fnm = "e13"
##    fnm = "pumsb_star"
##    fnm = "adultrain"
    d = Dataset(fnm)
    if fnm != "e13":
        exit(5)
    tr_a = d.occurncs['a']
    tr_c = d.occurncs['c']
    tr = tr_a & tr_c
    print(tr_a)
    print(tr_c)
    print(tr)
    print(d.inters(tr))
    
    
