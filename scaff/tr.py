d = dict()      
for i in range(5):
  d[i+1] = chr(ord('e') - i)
with open('../data/e24t.td', 'w') as g:
  with open('../data/e24.td') as f:
    for line in f:
      print(' '.join( sorted(d[int(i)] for i in line.split()) ), file = g)
