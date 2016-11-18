import sys
import numpy as np
from PIL import  Image

T1=10
T2=0.2
T3=0.2

def initPix2Reg():
	global height
	global width
	pix2reg=np.zeros((height, width), dtype=np.int)
	counter=0
	for i in xrange(height):
		for j in xrange(width):
			pix2reg[i][j]=counter
			counter+=1
	return pix2reg

def getReg2Pix(pix2reg):
	reg2pix={}
	for i in xrange(height):
		for j in xrange(width):
			if pix2reg[i][j] in reg2pix:
				reg2pix[pix2reg[i][j]].append((i,j))
			else:
				reg2pix[pix2reg[i][j]]=[(i,j)]
	return reg2pix

def drawReg(outputname, npim,reg2pix):
	global height
	global width
	regvalue={}
	for a,b in reg2pix.items():
		total=0
		for item in b:
			total+=npim[item[0]][item[1]]
		regvalue[a]=total/len(b)#int division
	newim=Image.new('L',(width, height), 0)
	newpix=newim.load()
	for a,b in reg2pix.items():
		for item in b:
			newpix[item[1], item[0]]=regvalue[a]
	newim.save(outputname)
	return

def weakCrackMerge(pix2reg, reg2pix, supergrid):
	global height
	global width
	for i in xrange(height):
		for j in xrange(width-1):
			left=pix2reg[i][j]
			right=pix2reg[i][j+1]
			if supergrid[2*i][2*j+1]<T1 and left!=right:
				for item in reg2pix[right]:
					pix2reg[item[0]][item[1]]=left
				reg2pix[left]=reg2pix[left]+reg2pix[right]
				del reg2pix[right]
	for i in xrange(height-1):
		for j in xrange(width):
			top=pix2reg[i][j]
			bottom=pix2reg[i+1][j]
			if supergrid[2*i+1][2*j]<T1 and top!=bottom:
				for item in reg2pix[bottom]:
					pix2reg[item[0]][item[1]]=top
				reg2pix[top]=reg2pix[top]+reg2pix[bottom]
				del reg2pix[bottom]
	return

def calInfo(pix2reg, reg2pix, supergrid):
	global height
	global width
	boundary={}
	perimeter={}
	neighbor={}
	for i in xrange(height):
		for j in xrange(width-1):
			left=pix2reg[i][j]
			right=pix2reg[i][j+1]
			if left!=right:
				if right<left:
					left, right=right, left
				###boundary
				if (left, right) not in boundary:
					boundary[(left, right)]=[1,0]
				else:
					boundary[(left, right)][0]+=1
				if supergrid[2*i][2*j+1]<T1:
					boundary[(left, right)][1]+=1
				###perimeter
				if left not in perimeter:
					perimeter[left]=1
				else:
					perimeter[left]+=1
				if right not in perimeter:
					perimeter[right]=1
				else:
					perimeter[right]+=1
				###neighbor
				if left not in neighbor:
					neighbor[left]={right:None}
				else:
					neighbor[left][right]=None
				if right not in neighbor:
					neighbor[right]={left:None}
				else:
					neighbor[right][left]=None
	for i in xrange(height-1):
		for j in xrange(width):
			top=pix2reg[i][j]
			bottom=pix2reg[i+1][j]
			if top!=bottom:
				if bottom<top:
					top, bottom=bottom, top
				###boundary
				if (top, bottom) not in boundary:
					boundary[(top, bottom)]=[1,0]
				else:
					boundary[(top, bottom)][0]+=1
				if supergrid[2*i+1][2*j]<T1:
					boundary[(top, bottom)][1]+=1
				###perimeter
				if top not in perimeter:
					perimeter[top]=1
				else:
					perimeter[top]+=1
				if bottom not in perimeter:
					perimeter[bottom]=1
				else:
					perimeter[bottom]+=1
				###neighbor
				if top not in neighbor:
					neighbor[top]={bottom:None}
				else:
					neighbor[top][bottom]=None
				if bottom not in neighbor:
					neighbor[bottom]={top:None}
				else:
					neighbor[bottom][top]=None
	return neighbor, boundary, perimeter

def mergeWithInfo(ra, rb):
	global pix2reg
	global reg2pix
	global perimeter
	global boundary
	global neighbor
	if rb < ra:
		ra, rb=rb, ra
	#update perimeter
	perimeter[ra]=perimeter[ra]+perimeter[rb]-2*boundary[(ra,rb)][0]
	del perimeter[rb]
	#update boundary
	#print '###'
	for nei in neighbor[rb]:
		bsmall=rb
		bbig=nei
		asmall=ra
		abig=nei
		if bsmall > bbig:
			bsmall, bbig= bbig, bsmall
		if asmall > abig:
			asmall, abig= abig, asmall
		if ra==nei:
			continue
		neighbor[ra][nei]=None
		neighbor[nei][ra]=None
		del neighbor[nei][rb]
		if (asmall, abig) in boundary:
			boundary[(asmall, abig)][0]+=boundary[(bsmall, bbig)][0]
			boundary[(asmall, abig)][1]+=boundary[(bsmall, bbig)][1]
		else:
			#print bsmall, bbig
			boundary[(asmall, abig)]=boundary[(bsmall, bbig)][:]
		del boundary[(bsmall, bbig)]
	del neighbor[ra][rb]
	del boundary[(ra,rb)]
	
	for item in reg2pix[rb]:
		pix2reg[item[0]][item[1]]=ra
	reg2pix[ra]=reg2pix[ra]+reg2pix[rb]
	del reg2pix[rb]
	

def perimeterRemove():
	global perimeter
	global boundary
	global pix2reg
	global T2
	flag=False
	for i in xrange(height):
		for j in xrange(width-1):
			left=pix2reg[i][j]
			right=pix2reg[i][j+1]
			if left!=right:
				if right<left:
					left, right=right, left
				if float(boundary[(left, right)][1])/min(perimeter[left],perimeter[right])>=T2:
					mergeWithInfo(left, right)
					flag=True
	for i in xrange(height-1):
		for j in xrange(width):
			top=pix2reg[i][j]
			bottom=pix2reg[i+1][j]
			if top!=bottom:
				if bottom<top:
					top, bottom=bottom, top
				if float(boundary[(top, bottom)][1])/min(perimeter[top], perimeter[bottom])>=T2:
					mergeWithInfo(top, bottom)
					flag=True
	return flag

def boundaryRemove():
	global boundary
	global pix2reg
	global T2
	flag=False
	for i in xrange(height):
		for j in xrange(width-1):
			left=pix2reg[i][j]
			right=pix2reg[i][j+1]
			if left!=right:
				if right<left:
					left, right=right, left
				if float(boundary[(left, right)][1])/float(boundary[(left, right)][0])>=T3:
					#print '#####'
					mergeWithInfo(left, right)
					flag=True
	for i in xrange(height-1):
		for j in xrange(width):
			top=pix2reg[i][j]
			bottom=pix2reg[i+1][j]
			if top!=bottom:
				if bottom<top:
					top, bottom=bottom, top
				if float(boundary[(top, bottom)][1])/float(boundary[(top, bottom)][0])>=T3:
					#print '#####'
					mergeWithInfo(top, bottom)
					flag=True
	return flag
	

imagename=sys.argv[1]
im=Image.open(imagename).convert('L')
npim=np.array(im)
height=npim.shape[0]
width=npim.shape[1]
supergrid=np.zeros((height*2+1, width*2+1), dtype=np.int)
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i][2*j]=npim[i][j]
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i+1][2*j]=abs(supergrid[2*i][2*j]-supergrid[2*i+2][2*j])
		supergrid[2*i][2*j+1]=abs(supergrid[2*i][2*j]-supergrid[2*i][2*j+2])

pix2reg=initPix2Reg()
reg2pix=getReg2Pix(pix2reg)
#drawReg(imagename.split('.jpeg')[0]+'.wcmerge.bmp', npim, reg2pix)
neighbor, boundary, perimeter=calInfo(pix2reg, reg2pix, supergrid)
#print perimeter
flag=True
while flag:
	flag=perimeterRemove()
drawReg(imagename.split('.jpeg')[0]+'.perimeter.bmp', npim, reg2pix)
flag=True
#for a, b in boundary.items():
	#if b[1]!=0:
		#print a,boundary[a]
while flag:
	flag=boundaryRemove()
drawReg(imagename.split('.jpeg')[0]+'.boundary.bmp', npim, reg2pix)
