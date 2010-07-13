"""

Project: yacaree
Programmer: JLB

Module encompassing some static objects

scale: for writing ints as floats with controlled precision loss

never: swallow three parameters and return False
(ToDo: make it swallow any number of parameters)

powset: iterator over all the subsets of the given set

"""

scale = 100000

confthr = int((2.0/3) * scale)

def never(n,s,t):
    return False

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

