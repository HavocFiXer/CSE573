import numpy as np
import cPickle as cp
from PIL import Image
import sys

imagename=sys.argv[1]

im=Image.open(imagename)
width=im.size[0]
height=im.size[1]
pix=im.load()

outfile=open(imagename+'.magnitude.txt','w')
magnitude=np.zeros((height, width))
logmag=np.zeros((height,width))
logmagmax=0.0
phase=np.zeros((height,width))

for u in xrange(height):
	print u
	for v in xrange(width):
		rtmp=0.0
		itmp=0.0
		for m in xrange(height):
			for n in xrange(width):
				ex=-2.0*np.pi*(float(u*m)/height+float(v*n)/width)
				rtmp+=np.cos(ex)*pix[n,m]
				itmp+=np.sin(ex)*pix[n,m]
		rtmp/=width*height
		itmp/=width*height
		#print 'rtmp->', rtmp
		#print 'itmp->', itmp
		magnitude[u][v]=np.sqrt(np.power(rtmp,2)+np.power(itmp,2))
		outfile.write('%f '%magnitude[u][v])
		logmag[u][v]=np.log10(magnitude[u][v]+1)
		if logmag[u][v]>logmagmax:
			logmagmax=logmag[u][v]
		phase[u][v]=np.arctan2(itmp,rtmp)
	outfile.write('\n')

f=file(imagename+'.mp.data','w')
cp.dump([magnitude,phase],f)
f.close()
	
outfile.close()

newim=Image.new('L',(width,height),0)
newpix=newim.load()
for u in xrange(height):
	for v in xrange(width):
		newpix[v,u]=int(logmag[(u+height/2)%height][(v+width/2)%width]/logmagmax*255)
newim.save(imagename+'.dft.bmp')
