import sys
import numpy as np
from PIL import  Image

imagename=sys.argv[1]

im=Image.open(imagename).convert('L')
npim=np.array(im)
#print npim
#print npim.dtype
height=npim.shape[0]
width=npim.shape[1]
supergrid=np.zeros((height*2+1, width*2+1), dtype=np.int)
#im.save(imagename.split('.jpeg')[0]+'.gray.bmp')
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i][2*j]=npim[i][j]
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i+1][2*j]=abs(supergrid[2*i][2*j]-supergrid[2*i+2][2*j])
		supergrid[2*i][2*j+1]=abs(supergrid[2*i][2*j]-supergrid[2*i][2*j+2])
outfile=open(imagename.split('.jpeg')[0]+'.supergrid.txt','w')
for i in xrange(2*height+1):
	for j in xrange(2*width+1):
		outfile.write('%d '%(supergrid[i][j]))
	outfile.write('\n')
outfile.close()
