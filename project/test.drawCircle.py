import sys
import cPickle as cp
from PIL import Image

beginr=int(sys.argv[1])
endr=int(sys.argv[2])
infilename=sys.argv[3]
newim=Image.new('L',(520, 520), 255)
newpix=newim.load()
x=260
y=260
f=file(infilename)
circle=cp.load(f)
f.close()
for i in xrange(beginr, endr+1):
	if (i%4)!=0:
		continue
	points=circle[i]
	for item in points:
		newpix[y+item[1], x+item[0]]=0
newim.save('testCircle%d-%d.jpg'%(beginr, endr))
