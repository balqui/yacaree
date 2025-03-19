'''
yacaree

Current revision: mid / late Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Read in a transactional dataset from a txt file,
one transaction per line.

To merge some day with equivalent fragments of degais and/or PyDaMElo.

items in each transaction separated by whitespace
 as per string method split()
whitespace characters as per split() cannot occur
 inside the items
empty transactions are ignored
dataset replicated into two ddicts:
 transcns: set of items per transaction id (unsigned, starts at zero)
 occurncs: set of transaction ids per item
also:
 scale (CAVEAT: maybe to migrate somewhere else)
 nrits - number of items
 nrtr  - number of transactions
 nrocc - number of occurrences
 univ  - universe of items
 dataset filename
 datasetfile, closed, should one need to open it again
'''

from collections import defaultdict

from iface import IFace

class Dataset:

    def __init__(self):
        "find actual file, already open, and read the dataset in - redundancies left"
        IFace.report("Reading in dataset from file " +
                     IFace.datafile.name)
        self.nrocc = 0
        self.nrtr = 0
        self.univ = set()
        self.transcns = defaultdict(set)
        self.occurncs = defaultdict(set)
        for line in IFace.datafile:
            isempty = True
            for el in line.strip().split():
                if len(el) > 0:
                    isempty = False
                    self.nrocc += 1
                    self.univ.add(el)
                    self.transcns[self.nrtr].add(el)
                    self.occurncs[el].add(self.nrtr)
            if not isempty:
                self.nrtr += 1
        self.nrits = len(self.univ)
        IFace.hpar.nrtr = self.nrtr
        IFace.hpar.nrits = self.nrits
        IFace.datafile.close()
        IFace.report("Dataset read in. Consists of " +
            str(self.nrtr) + " transactions from among " +
            str(self.nrits) + " different items, with a total of " +
            str(self.nrocc) + " item occurrences.")

    def inters(self, lstr):
        "for iterable of transactions lstr, return their intersection"
        items = self.univ.copy()
        for t in lstr:
            items &= self.transcns[t]
        return items

    def slow_supp(self, st):
        """
        Find the supporting set of st in ds by means of a full scan.
        Hopefully it is infrequent to need to resort to this slow way.
        CAVEAT: Consider keeping a count of calls to this method.
        """
        exact = False # did it match exactly some transaction?
        transcontain = list()
        for tr in self.transcns:
            if st <= self.transcns[tr]:
                transcontain.append(tr)
                if self.transcns[tr] <= st:
                    exact = True
        return transcontain, exact


if __name__ == "__main__":

    from filenames import FileNames

    # ~ fnm = "data/e13"
    fnm = "data/toy"
    # ~ fnm = "data/adultrain"

    IFace.fn = FileNames(IFace)
    IFace.opendatafile(fnm)
    d = Dataset()
    a, c = 'A', 'C'
    # ~ a, c = 'a', 'c'
    tr_a = d.occurncs[a]
    tr_c = d.occurncs[c]
    # ~ tr_a = d.occurncs['Black']
    # ~ tr_c = d.occurncs['Doctorate']
    tr = tr_a & tr_c
    print(tr_a)
    print(tr_c)
    print(tr)
    print(d.inters(tr))
    
    
