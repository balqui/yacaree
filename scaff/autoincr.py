"""
Autoincrement class to label differently each itemset created,
needed for comparison purposes; moved out of the class at the
time I tried to get ItSet's to be @dataclasses (see itset_dc.py).
Also, a good learning opportunity: reversing the order of the
decorators does not work.
"""

class AIncr:

    _label = 0

    @classmethod
    @property
    def label(cls):
        cls._label += 1
        return cls._label

