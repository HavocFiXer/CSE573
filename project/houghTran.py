import sys
import numpy as np
import cPickle as cp
import scipy.signal
import os
from PIL import Image, ImageFilter

edgeThreshold=120
counterCut=10
#maxrad
#minrad

imagename=sys.argv[1]
circlename=sys.argv[2]
gaussian=np.array([	[1.0/16.0, 1.0/8.0, 1.0/16.0],
					[ 1.0/8.0, 1.0/4.0,  1.0/8.0],
					[1.0/16.0, 1.0/8.0, 1.0/16.0]])
im=Image.open(imagename).convert('L')
im.save(imagename.split('.jpg')[0]+'.black.jpg')

npim=np.array(im)
npdenoise=scipy.signal.convolve2d(npim, gaussian, mode='same')
height=npdenoise.shape[0]
width=npdenoise.shape[1]
denoiseim=Image.fromarray(np.uint8(npdenoise))
denoiseim.save(imagename.split('.jpg')[0]+'.gaussian.jpg')

edgeim=denoiseim.filter(ImageFilter.FIND_EDGES)
edgeim.save(imagename.split('.jpg')[0]+'.edge.jpg')

edgepoints=[]
edgepix=edgeim.load()
for i in xrange(height):
	for j in xrange(width):
		if(edgepix[j,i]<edgeThreshold):
			edgepix[j,i]=255
			#edgepoints.append((i,j))
		else:
			edgepix[j,i]=0
			edgepoints.append((i,j))
edgeim.save(imagename.split('.jpg')[0]+'.edge.bmp')

maxrad=max(height, width)/2
minrad=3

f=file(circlename)
circle=cp.load(f)
f.close()

os.system('mkdir %s'%(imagename.split('.jpg')[0]))
outfile=open(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.stat.txt','w')
for rad in xrange(minrad, maxrad+1):
	print 'rad: ', rad
	counter=np.zeros((3*height, 3*width), dtype=np.int)
	points=circle[rad]
	stat={}
	for pair in edgepoints:
		for delta in points:
			counter[height+pair[0]+delta[0]][width+pair[1]+delta[1]]+=1
	subcounter=counter[height:2*height,width:2*width]
	for i in xrange(height):
		for j in xrange(width):
			if subcounter[i][j]>counterCut:
				if subcounter[i][j] not in stat:
					stat[subcounter[i][j]]=1
				else:
					stat[subcounter[i][j]]+=1
			if subcounter[i][j] > 255:
				subcounter[i][j]=255
	heatmap=Image.fromarray(np.uint8(subcounter))
	heatmap.save(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.heatmap.%d.jpg'%(rad))
	statlist=sorted(stat.iteritems(), key=lambda asd:asd[0], reverse=True)
	outfile.write('rad%d->'%(rad))
	for item in statlist:
		outfile.write('%d:%d\t'%(item[0], item[1]))
	outfile.write('\n')
outfile.close()
