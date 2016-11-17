from PIL import Image
import sys

name1=sys.argv[1]
name2=sys.argv[2]

im1=Image.open(name1)
width1=im1.size[0]
height1=im1.size[1]
pix1=im1.load()

im2=Image.open(name2)
width2=im2.size[0]
height2=im2.size[1]
pix2=im2.load()

if width1!=width2 or height1!=height2:
	print 'images are not in the same size'
	exit()

mse=0
for i in xrange(height1):
	for j in xrange(width1):
		mse+=(pix1[j,i]-pix2[j,i])**2

print 'MSE:', mse
