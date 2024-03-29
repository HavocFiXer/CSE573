import sys
import numpy as np
from PIL import  Image

T1=15

def initPix2Reg(npim, supergrid):
	global T1
	height=npim.shape[0]
	width=npim.shape[1]
	pix2reg=np.zeros((height, width), dtype=np.int)
	counter=1
	for j in xrange(width-1):
		if supergrid[0][2*j+1]<T1:
			pix2reg[0][j+1]=pix2reg[0][j]
		else:
			pix2reg[0][j+1]=counter
			counter+=1
	for i in xrange(height-1):
		for j in xrange(width):
			if supergrid[2*i+1][2*j]<T1:
				pix2reg[i+1][j]=pix2reg[i][j]
			elif j==0:
				pix2reg[i+1][j]=counter
				counter+=1
			elif supergrid[2*i+2][2*j-1]<T1:
				pix2reg[i+1][j]=pix2reg[i+1][j-1]
			else:
				pix2reg[i+1][j]=counter
				counter+=1
	#######for test#######
	global imagename
	outfile=open(imagename.split('.jpeg')[0]+'.pix2reg.txt','w')
	for i in xrange(height):
		for j in xrange(width):
			outfile.write('%d '%(pix2reg[i][j]))
		outfile.write('\n')
	outfile.close()
	######################
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
	height=npim.shape[0]
	width=npim.shape[1]
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

imagename=sys.argv[1]
im=Image.open(imagename).convert('L')
npim=np.array(im)
height=npim.shape[0]
width=npim.shape[1]
supergrid=np.zeros((height*2+1, width*2+1), dtype=np.int)
#newim=Image.new('L',(width, height), 0)
#newpix=newim.load()
#im.save(imagename.split('.jpeg')[0]+'.gray.bmp')
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i][2*j]=npim[i][j]
for i in xrange(height):
	for j in xrange(width):
		supergrid[2*i+1][2*j]=abs(supergrid[2*i][2*j]-supergrid[2*i+2][2*j])
		supergrid[2*i][2*j+1]=abs(supergrid[2*i][2*j]-supergrid[2*i][2*j+2])

pix2reg=initPix2Reg(npim, supergrid)
reg2pix=getReg2Pix(pix2reg)
drawReg(imagename.split('.jpeg')[0]+'.region.bmp', npim, reg2pix)

'''
reg2pix={}
weak={}
boundary={}
perimeter={}
counter=0
for i in xrange(height):
	for j in xrange(width):
		pix2reg[i][j]=counter
		reg2pix[counter]={(i,j):None}
		perimeter[counter]=4
		counter+=1
for i in xrange(height):
	perimeter[pix2reg[i][0]]-=1
	perimeter[pix2reg[i][width-1]]-=1
for j in xrange(width):
	perimeter[pix2reg[0][j]]-=1
	perimeter[pix2reg[height-1][j]]-=1
'''
