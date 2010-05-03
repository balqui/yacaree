"""

Project: yacaree
Programmer: JLB

Description: module encompassing static values for the whole run

scale: for writing ints as floats with controlled precision loss
nrtr: dataset size (number of transactions)
nrits: universe size (number of different items)
nrocc: total number of item occurrences in dataset

powset: iterator over all the subsets of the given set

"""

scale = 100000

nrtr = 0

nrits = 0

nratt = 0

def powset(aset):
    "iterator on the powerset of given aset"
    if len(aset)==0:
        yield set([])
    else:
        e = aset.pop()
        for s in powset(aset):
            s.add(e)
            yield s
            s.discard(e)
            yield s

## usage: for e in powset(set(range(5))): print e


