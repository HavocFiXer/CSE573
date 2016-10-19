from PIL import Image
import sys

imagename=sys.argv[1]

im=Image.open(imagename)
width=im.size[0]
height=im.size[1]
pix=im.load()

outfile=open(imagename+'.txt', 'w')
for i in xrange(height):
	for j in xrange(width):
		outfile.write('%d '%pix[j,i])
	outfile.write('\n')
		

#newim=Image.new('L',(width,height),0)
outfile.close()
