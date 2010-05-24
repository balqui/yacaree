"""

Project: yacaree
Programmer: JLB

Description: module encompassing static values for the whole run

scale: for writing ints as floats with controlled precision loss

nrtr: dataset size (number of transactions)
nrits: universe size (number of different items)
nrocc: total number of item occurrences in dataset
BUT THESE FOUR VALUES HAVE MOVED TO Dataset CLASS,
UNCLEAR WHAT SHOULD HAPPEN TO scale

powset: iterator over all the subsets of the given set

openfile: catch exception if not readable - MOVED TO iface

"""

scale = 100000

##nrtr = 0
##
##nrits = 0
##
##nratt = 0

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

##def openfile(filename):
##    try:
##        f = open(filename)
##        f.readline()
##        f.close
##        return open(filename)
##    except (IOError, OSError):
##        reporterror("nonexistent or unreadable file")

