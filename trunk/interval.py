"""
Project: yacaree
Programmer: JLB

Description: float values of parameters (eg confidence boost)
may not be fully known at a given time, just upper and lower
bounds; stored as ints wrt statics.scale, convert to floats
just for output.

To do: raise an exception if lower bound above upper bound?
"""

from statics import scale

class interval:
    """
    interval of int values candidate for a parameter
    """

    def __init__(self,lbd,ubd):
        self.lbd = lbd
        self.ubd = ubd

    def reset(self,lbd=None,ubd=None):
        if lbd is not None:
            self.lbd = lbd
        if ubd is not None:
            self.ubd = ubd

    def revise(self,lbd=None,ubd=None):
        "like reset, but only shrink of interval allowed, o/w stays equal"
        if lbd is not None:
            if self.lbd <= lbd <= self.ubd:
                self.lbd = lbd
        if ubd is not None:
            if self.lbd <= ubd <= self.ubd:
                self.ubd = ubd

    def __str__(self):
        if self.lbd == self.ubd:
            return str(float(self.lbd)/scale)
        else:
            return str(float(self.lbd)/scale)+","+str(float(self.ubd)/scale)
 
if __name__=="__main__":

    from iface import iface

    iface.report("scale is:"+str(scale),0)

    p = interval(-10*scale,12*scale)

    iface.report("scaled interval [-10,12]:"+str(p),0)

    p.reset(0,scale/2)

    iface.report("interval [0,scale/2]:"+str(p),0)

    p.revise(100,scale/100)

    iface.report("revised [100,scale/100]:"+str(p),0)

    p.reset(0,scale)

    p.revise(lbd=100)

    iface.report("[0,1] revised lbd 100/scale:"+str(p),0)

    p.revise(ubd=1000)

    iface.report("then revised ubd 1000/scale:"+str(p),0)

    p.revise(lbd=1000)

    iface.report("then revised lbd 1000/scale:"+str(p),0)

    
