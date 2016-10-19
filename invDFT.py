import numpy as np
import cPickle as cp
from PIL import Image
import sys

dataname=sys.argv[1]

f=file(dataname)
data=cp.load(f)
f.close()

magnitude=data[0]
phase=data[1]
height=magnitude.shape[0]
width=magnitude.shape[1]
fcos=np.zeros(magnitude.shape)
fsin=np.zeros(magnitude.shape)

space=np.zeros(magnitude.shape)
minspace=10000000.0
maxspace=0.0

for u in xrange(height):
	for v in xrange(width):
		fcos[u][v]=magnitude[u][v]*np.cos(phase[u][v])
		fsin[u][v]=magnitude[u][v]*np.sin(phase[u][v])

for m in xrange(height):
	for n in xrange(width):
		rtmp=0.0
		itmp=0.0
		for u in xrange(height):
			for v in xrange(width):
				ex=2.0*np.pi*(float(u*m)/height+float(v*n)/width)
				vcos=np.cos(ex)
				vsin=np.sin(ex)
				rtmp+=fcos[u][v]*vcos-fsin[u][v]*vsin
				itmp+=fcos[u][v]*vsin+fsin[u][v]*vcos
		space[m][n]=np.sqrt(np.power(rtmp,2)+np.power(itmp,2))
		if space[m][n]>maxspace:
			maxspace=space[m][n]
		if space[m][n]<minspace:
			minspace=space[m][n]

#print maxspace
#print minspace
newim=Image.new('L',(width,height),0)
newpix=newim.load()
for m in xrange(height):
	for n in xrange(width):
		newpix[n,m]=int(space[m][n])#int((space[m][n]-minspace)/(maxspace-minspace)*255)
newim.save(dataname.split('.mp')[0]+'.idft.bmp')
