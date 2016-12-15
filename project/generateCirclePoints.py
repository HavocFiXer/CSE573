import sys
import cPickle as cp
from PIL import Image

begin=int(sys.argv[1])
end=int(sys.argv[2])
circle={}

def drawCircle(radius):
	global circle
	points=[]
	x=radius
	y=0
	err=0
	while(x>y):
		points.append((x,y))
		points.append((y,x))
		points.append((-x,y))
		points.append((-y,x))
		points.append((-x,-y))
		points.append((-y,-x))
		points.append((x,-y))
		points.append((y,-x))
		y+=1
		err+=1+2*y
		if(2*(err-x)+1>0):
			x-=1
			err+=1-2*x
	circle[radius]=points
	return

for i in xrange(begin, end+1):
	drawCircle(i)

f=file('Circle%d-%d.data'%(begin,end),'w')
cp.dump(circle,f)
f.close()
