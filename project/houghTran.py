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

maxrad=max(height, width)/2
minrad=7

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
	sd=0.0
	mean=0.0
	number=0
	for i in xrange(height):
		for j in xrange(width):
			if subcounter[i][j]>counterCut:
				mean+=subcounter[i][j]
				sd+=subcounter[i][j]*subcounter[i][j]
				number+=1
				if subcounter[i][j] not in stat:
					stat[subcounter[i][j]]=1
				else:
					stat[subcounter[i][j]]+=1
	for i in xrange(height):
		for j in xrange(width):
			if subcounter[i][j] > 255:
				subcounter[i][j]=255
	heatmap=Image.fromarray(np.uint8(subcounter))
	heatmap.save(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.heatmap.%d.jpg'%(rad))
	statlist=sorted(stat.iteritems(), key=lambda asd:asd[0], reverse=True)
	if number==0:
		mean=0.0
	else:
		mean=mean/float(number)/float(rad)
	if number<=1:
		sd=0.0
	else:
		sd=(sd/float(number-1))**0.5/float(rad)
	outfile.write('rad%d=> mean:%f, sd:%f, 3sigma: %f->'%(rad, mean, sd, mean+3*sd))
	for item in statlist:
		outfile.write('%f:%d\t'%(float(item[0])/float(rad), item[1]))
	outfile.write('\n')
outfile.close()
