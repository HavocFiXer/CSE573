import sys
import numpy as np
import scipy.signal
from PIL import  Image

imagename=sys.argv[1]

core=np.array([ [0,  0,  1,  0,  0],
				[0,  1,  2,  1,  0],
				[1,  2,-16,  2,  1],
				[0,  1,  2,  1,  0],
				[0,  0,  1,  0,  0] ])
im=Image.open(imagename).convert('L')
npim=np.array(im)
newnpim=scipy.signal.convolve2d(npim, core, mode='same')
height=newnpim.shape[0]
width=newnpim.shape[1]
newim=Image.new('L',(width, height), 0)
newpix=newim.load()
for i in xrange(height-1):
	for j in xrange(width-1):
		negative=0
		for a in xrange(2):
			for b in xrange(2):
				if newnpim[i+a][j+b]<0:
					negative+=1
		#print negative
		if negative <4 and negative!=0:
			newpix[j,i]=0
		else:
			newpix[j,i]=255
newim.save(imagename.split('.jpeg')[0]+'.LoGcrossing.jpeg')
