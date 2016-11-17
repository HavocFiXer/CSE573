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

def gaussianfunc(origin):
	blur=np.array([[1.0/16, 1.0/8, 1.0/16],[1.0/8, 1.0/4, 1.0/8],[1.0/16, 1.0/8, 1.0/16]])
	height=origin.shape[0]
	width=origin.shape[1]
	gaussian=np.zeros((height,width), np.int16)
	for i in xrange(height):
		gaussian[i][0]=origin[i][0]
		gaussian[i][width-1]=origin[i][width-1]
	for j in xrange(width):
		gaussian[0][j]=origin[0][j]
		gaussian[height-1][j]=origin[height-1][j]
	for i in xrange(1, height-1):
		for j in xrange(1, width-1):
			gaussian[i][j]=int(sum(sum(np.array([[origin[i-1][j-1],origin[i-1][j],origin[i-1][j+1]],[origin[i][j-1],origin[i][j],origin[i][j+1]],[origin[i+1][j-1],origin[i+1][j],origin[i+1][j+1]]]*blur))))
	return gaussian

def downfunc(origin):
	height=origin.shape[0]/2
	width=origin.shape[1]/2
	down=np.zeros((height,width), np.int16)
	for i in xrange(height):
		for j in xrange(width):
			#down[i][j]=origin[2*i][2*j]#min([origin[2*i][2*j],origin[2*i+1][2*j],origin[2*i][2*j+1],origin[2*i+1][2*j+1]])
			down[i][j]=min([origin[2*i][2*j],origin[2*i+1][2*j],origin[2*i][2*j+1],origin[2*i+1][2*j+1]])
	return down

def upfunc(origin):
	height=origin.shape[0]*2
	width=origin.shape[1]*2
	up=np.zeros((height,width), np.int16)
	for i in xrange(height):
		for j in xrange(width):
			up[i][j]=origin[i/2][j/2]
	return up

def laplacianfunc(origin, up):
	height=origin.shape[0]
	width=origin.shape[1]
	laplacian=np.zeros((height,width), np.int16)
	for i in xrange(height):
		for j in xrange(width):
			laplacian[i][j]=int(origin[i][j]-up[i][j])
	return laplacian


imagename=sys.argv[1]
origin=loadimagefunc(imagename)
dumpdata=[]

for level in xrange(1,6):
	gaussian=gaussianfunc(origin)
	saveimagefunc(gaussian, imagename+'.'+str(level)+'.gaussian.bmp')
	down=downfunc(gaussian)
	saveimagefunc(down, imagename+'.'+str(level)+'.downsampling.bmp')
	up=upfunc(down)
	saveimagefunc(up, imagename+'.'+str(level)+'.upsampling.bmp')
	laplacian=laplacianfunc(origin, up)
	dumpdata.append(laplacian)
	saveimagefunc(laplacian, imagename+'.'+str(level)+'.laplacian.bmp')
	origin=np.copy(down)
	
f=file('LaplacianPyramid.data','w')
cp.dump(dumpdata,f)
f.close()
