from PIL import Image
import numpy as np
import sys

imagename=sys.argv[1]
im=Image.open(imagename)
width=im.size[0]
height=im.size[1]
pix=im.load()

pixlist=[]
for i in xrange(height):
	pixlist.append([])
	for j in xrange(width):
		pixlist[i].append(pix[j,i])
pixarray=np.array(pixlist)

dftarray=np.fft2(pixarray)

outfile=open(imagename+'.standardDFT.txt', 'w')
for i in xrange(height):
	for j in xrange(width):
		outfile.write('%f '%dftarray[i][j])
	outfile.write('\n')
outfile.close()
