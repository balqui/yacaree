class S(set):
   cnt = 0
   def __init__(self, c = set()):
     super().__init__(c)
     S.cnt += 1
     self.t = S.cnt
   def __str__(self):
     return ', '.join(str(e) for e in self) + ' [' + str(self.t) + ']'
 
a = S()
b = S(range(4))
c = S(['h', 'i', 'j'])
print(a)
print(b)
print(c)
d = S(a|b|c)
print(d)
