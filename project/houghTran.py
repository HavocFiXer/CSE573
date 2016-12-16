import sys
import numpy as np
import cPickle as cp
import scipy.signal
import os
#from skimage import filter
import skimage.filter
#from feature import canny
from PIL import Image, ImageFilter

edgeThreshold=120
counterCut=10
sig=3
low=50
high=90
impulseRate=0.7
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

npedge=skimage.filter.canny(npdenoise, sigma=sig, low_threshold=low, high_threshold=high)
npedge=np.where(npedge, 0, 255)
#edgeim=denoiseim.filter(ImageFilter.FIND_EDGES)
edgeim=Image.fromarray(np.uint8(npedge))
edgeim.save(imagename.split('.jpg')[0]+'.edge.sig%d.low%d.high%d.bmp'%(sig,low, high))

edgepoints=[]
for i in xrange(height):
	for j in xrange(width):
		if npedge[i][j]<=128:
			edgepoints.append((i,j))
		#if(npedge[i][j]<edgeThreshold):
			#npedge[i][j]=255
			#edgepoints.append((i,j))
		#else:
			#edgepix[j,i]=0
#edgeim.save(imagename.split('.jpg')[0]+'.edge.bmp')

#maxrad=max(height, width)/2
maxrad=100
minrad=7

f=file(circlename)
circle=cp.load(f)
f.close()

universe={}
os.system('mkdir %s'%(imagename.split('.jpg')[0]))
outfile=open(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.stat.txt','w')
for rad in xrange(minrad, maxrad+1):
	print 'rad: ', rad
	counter=np.zeros((3*height, 3*width), dtype=np.int)
	points=circle[rad]
	stat={}
	position={}
	for pair in edgepoints:
		for delta in points:
			counter[height+pair[0]+delta[0]][width+pair[1]+delta[1]]+=1
	subcounter=counter[height:2*height, width:2*width]
	for i in xrange(height):
		for j in xrange(width):
			if subcounter[i][j]>counterCut:
				if subcounter[i][j] not in stat:
					stat[subcounter[i][j]]=1
				else:
					stat[subcounter[i][j]]+=1
				if subcounter[i][j] not in position:
					position[subcounter[i][j]]=[(i,j)]
				else:
					position[subcounter[i][j]].append((i,j))
	statlist=sorted(stat.iteritems(), key=lambda asd:asd[0], reverse=True)
	outfile.write('rad%d=> '%(rad))
	for item in statlist:
		outfile.write('%f:%d\t'%(float(item[0])/float(rad), item[1]))
	outfile.write('\n')
	topstat=[]
	topposition=[]
	for i in xrange(7):
		topstat.append(float(statlist[i][0])/float(rad))
		topposition.append(position[statlist[i][0]][:])
	universe[rad]=(topstat, topposition)

	#generate heat map, will modify value, do it last
	for i in xrange(height):
		for j in xrange(width):
			if subcounter[i][j] > 255:
				subcounter[i][j]=255
	heatmap=Image.fromarray(np.uint8(subcounter))
	heatmap.save(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.heatmap.%d.jpg'%(rad))
outfile.close()

drawcircle=[]
for rad in xrange(minrad+3, maxrad-4):
	if universe[rad][0]*impulseRate>universe[rad-1][0]:
		nxt=0
		while nxt<4:
			if universe[rad+nxt][0]*impulseRate>universe[rad+nxt+1][0]:
				break
			nxt+=1
		if nxt<4:
			for i in xrange(0,nxt+1):
				for item in universe[rad+i][1]:
					drawcircle.append((item[0],item[1],rad))
			
