import sys
import numpy as np
import scipy.signal
from PIL import  Image

sobelThreshold=80

imagename=sys.argv[1]

core=np.array([ [ 0, 0,-1,-1,-1, 0, 0],
				[ 0,-2,-3,-3,-3,-2, 0],
				[-1,-3, 5, 5, 5,-3,-1],
				[-1,-3, 5,16, 5,-3,-1],
				[-1,-3, 5, 5, 5,-3,-1],
				[ 0,-2,-3,-3,-3,-2, 0],
				[ 0, 0,-1,-1,-1, 0, 0] ])
sobel1=np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
sobel2=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobel3=np.array([[0,1,2],[-1,0,1],[-2,-1,0]])
sobel4=np.array([[2,1,0],[1,0,-1],[0,-1,-2]])
im=Image.open(imagename).convert('L')
npim=np.array(im)
newnpim=scipy.signal.convolve2d(npim, core, mode='same')
height=newnpim.shape[0]
width=newnpim.shape[1]
sobel1np=scipy.signal.convolve2d(npim, sobel1, mode='same')
sobel2np=scipy.signal.convolve2d(npim, sobel2, mode='same')
sobel3np=scipy.signal.convolve2d(npim, sobel3, mode='same')
sobel4np=scipy.signal.convolve2d(npim, sobel4, mode='same')
newim=Image.new('L',(width, height), 0)
newpix=newim.load()
for i in xrange(height-1):
	for j in xrange(width-1):
		negative=0
		for a in xrange(2):
			for b in xrange(2):
				if newnpim[i+a][j+b]<0:
					negative+=1
		if negative <4 and negative!=0 and (abs(sobel1np[i][j])>=sobelThreshold or abs(sobel2np[i][j])>=sobelThreshold or abs(sobel3np[i][j])>=sobelThreshold or abs(sobel4np[i][j])>=sobelThreshold):
			newpix[j,i]=0
		else:
			newpix[j,i]=255
newim.save(imagename.split('.jpeg')[0]+'.DoGfdsupport.jpeg')
