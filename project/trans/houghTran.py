import sys
import numpy as np
import cPickle as cp
import scipy.signal
import os
import skimage.filter
from PIL import Image, ImageFilter, ImageDraw

configname=sys.argv[1]
configfile=open(configname,'r')
for line in configfile:
	seg=line.strip().split('=')
	if seg[0].strip()=='image_name':
		imagename=seg[1].strip()
	if seg[0].strip()=='circle_name':
		circlename=seg[1].strip()
	if seg[0].strip()=='counter_cut':
		counterCut=int(seg[1])
	if seg[0].strip()=='canny_sigma':
		sig=int(seg[1])
	if seg[0].strip()=='canny_low_threshold':
		low=int(seg[1])
	if seg[0].strip()=='canny_high_threshold':
		high=int(seg[1])
	if seg[0].strip()=='impulse_rate':
		impulseRate=float(seg[1])
	if seg[0].strip()=='drop_rate':
		dropRate=float(seg[1])
	if seg[0].strip()=='max_radius':
		maxrad=int(seg[1])
	if seg[0].strip()=='min_radius':
		minrad=int(seg[1])

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
edgeim.save(imagename.split('.jpg')[0]+'.edge.bmp')

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
		if i>=len(statlist):
			break
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
'''
for rad in xrange(minrad+3, maxrad-4):
	#print 'rad->', rad
	if len(universe[rad][0])<1 or len(universe[rad-1][0])<1:
		continue
	#print universe[rad][0][0]*impulseRate,universe[rad-1][0][0]
	if universe[rad][0][0]*impulseRate>universe[rad-1][0][0]:
		#print '   ->',universe[rad][0][0]*impulseRate,universe[rad-1][0][0]
		nxt=0
		while nxt<4:
			if len(universe[rad+nxt+1][0])<1 or universe[rad+nxt][0][0]*impulseRate>universe[rad+nxt+1][0][0]:
				break
			nxt+=1
		if nxt<4:
			#print 'yes'
			for i in xrange(0,nxt+1):
				for item in universe[rad+i][1][0]:
					drawcircle.append((item[0],item[1],rad))
for rad in xrange(minrad, maxrad+1):
	#print 'rad->', rad
	if len(universe[rad][0])<2:
		continue
	for i in xrange(0, 4):
		if i+1>=len(universe[rad][0]):
			break
		if universe[rad][0][i]*dropRate>universe[rad][0][i+1]:
			for item in universe[rad][1][i]:
				drawcircle.append((item[0],item[1],rad))
	
#combine circles
#print drawcircle
bucket=[]
#print len(drawcircle)
for cir in drawcircle:
	#print 'bucket->', bucket
	#print 'cir->', cir
	flag=True
	for i in xrange(len(bucket)):
		for item in bucket[i]:
			if abs(item[0]-cir[0])<3 and abs(item[1]-cir[1])<3 and abs(item[2]-cir[2])<6:
				bucket[i].append(cir)
				flag=False
				break
		if not flag:
			break
	if flag:
		bucket.append([cir])

drawcircle=[]
for slot in bucket:
	x=0
	y=0
	r=0
	for item in slot:
		x+=item[0]
		y+=item[1]
		r+=item[2]
	drawcircle.append((x/len(slot), y/len(slot), r/len(slot)))
'''
				
			
drawim=Image.open(imagename)
draw=ImageDraw.Draw(drawim)
for item in drawcircle:
	draw.ellipse((item[1]-item[2], item[0]-item[2], item[1]+item[2], item[0]+item[2]), fill=None, outline='blue')
drawim.save(imagename.split('.jpg')[0]+'.circles.jpg')
del draw

drawim=Image.new('RGB',(width,height),'white')
draw=ImageDraw.Draw(drawim)
for item in drawcircle:
	draw.ellipse((item[1]-item[2], item[0]-item[2], item[1]+item[2], item[0]+item[2]), fill=None, outline='blue')
drawim.save(imagename.split('.jpg')[0]+'.blank.jpg')
del draw
