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
#print core
#print sum(sum(core))
im=Image.open(imagename).convert('L')
#width=im.size[0]
#height=im.size[1]
#pix=im.load()
npim=np.array(im)
print npim
newnpim=scipy.signal.convolve2d(npim, core, mode='same')
print newnpim
#newim=Image.fromarray(newnpim)
height=newnpim.shape[0]
width=newnpim.shape[1]
outfile=open(imagename.split('.jpeg')[0]+'.corevalue.txt','w')
for i in xrange(height):
	for j in xrange(width):
		outfile.write('%d '%(newnpim[i][j]))
	outfile.write('\n')
outfile.close()
print 'height:', height
print 'width:', width
for i in xrange(height):
	for j in xrange(width):
		if newnpim[i][j]<0:
			newnpim[i][j]=255
		else:
			newnpim[i][j]=0
newim=Image.fromarray(newnpim,'L')
newim.save(imagename.split('.jpeg')[0]+'.bi.bmp')
print 'height:', newim.size[1]
print 'width:', newim.size[0]
