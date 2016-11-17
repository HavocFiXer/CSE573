from PIL import Image
import numpy as np
import cPickle as cp
import sys

def saveimagefunc(arr, name):
	height=arr.shape[0]
	width=arr.shape[1]
	im=Image.new('L', arr.shape, 0)
	pix=im.load()
	for i in xrange(height):
		for j in xrange(width):
			pix[j,i]=int(arr[i][j])
	im.save(name)

def loadimagefunc(imagename):
	im=Image.open(imagename)
	width=im.size[0]
	height=im.size[1]
	pix=im.load()
	origin=np.zeros((height,width),np.int16)
	for i in xrange(height):
		for j in xrange(width):
			origin[i][j]=pix[j,i]
	return origin

def upfunc(origin):
	height=origin.shape[0]*2
	width=origin.shape[1]*2
	up=np.zeros((height,width), np.int16)
	for i in xrange(height):
		for j in xrange(width):
			up[i][j]=origin[i/2][j/2]
	return up

def recoverfunc(origin, laplacian):
	height=origin.shape[0]
	width=origin.shape[1]
	recover=np.zeros((height,width), np.int16)
	for i in xrange(height):
		for j in xrange(width):
			recover[i][j]=int(origin[i][j]+laplacian[i][j])
	return recover


f=file('LaplacianPyramid.data')
laplacian=cp.load(f)
f.close()
gaussian=loadimagefunc(sys.argv[1])
up=upfunc(gaussian)
recover=recoverfunc(up, laplacian[4])
up=upfunc(recover)
recover=recoverfunc(up, laplacian[3])
up=upfunc(recover)
recover=recoverfunc(up, laplacian[2])
up=upfunc(recover)
recover=recoverfunc(up, laplacian[1])
up=upfunc(recover)
recover=recoverfunc(up, laplacian[0])

saveimagefunc(recover, sys.argv[1]+'.rev.bmp')
