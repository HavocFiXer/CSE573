import sys
import numpy as np
import scipy.signal
from PIL import  Image

imagename=sys.argv[1]

core=np.array([ [ 0, 0,-1,-1,-1, 0, 0],
				[ 0,-2,-3,-3,-3,-2, 0],
				[-1,-3, 5, 5, 5,-3,-1],
				[-1,-3, 5,16, 5,-3,-1],
				[-1,-3, 5, 5, 5,-3,-1],
				[ 0,-2,-3,-3,-3,-2, 0],
				[ 0, 0,-1,-1,-1, 0, 0] ])
im=Image.open(imagename).convert('L')
npim=np.array(im)
newnpim=scipy.signal.convolve2d(npim, core, mode='same')
height=newnpim.shape[0]
width=newnpim.shape[1]
newim=Image.new('L',(width, height), 0)
newpix=newim.load()
for i in xrange(height):
	for j in xrange(width):
		if newnpim[i][j]<=0:
			newpix[j,i]=0
		else:
			newpix[j,i]=255
newim.save(imagename.split('.jpeg')[0]+'.DoG.jpeg')
