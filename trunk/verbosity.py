"""
Project: yacaree
Package: verbosity - deprecated
Programmers: JLB

potergeist module to employ the slatt clattice module
on top of the iface yacaree module instead of the
original slatt verbosity module
"""

from iface import iface

class verbosity:
    """
    Offers messaging of what is ongoing and ascii-based progress report
    Everything can be put off through the verbosity level
    """

    def __init__(self,verb=True):
        iface.repong()
        if verb:
            "useless as of today"
            iface.verb = 3
        else:
            iface.verb = 1

    def messg(self,s):
        iface.say(s)

    def inimessg(self,s):
        iface.report(s)

    def errmessg(self,s):
        iface.reportwarning(s)

    def zero(self,newlim=0):
        iface.repong(newlim)

    def tick(self):
        iface.pong()

    def __str__(self):
        return ""

