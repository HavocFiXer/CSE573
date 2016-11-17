import sys
from PIL import  Image

imagename=sys.argv[1]

im=Image.open(imagename).convert('L')
width=im.size[0]
height=im.size[1]
pix=im.load()
im.save(imagename.split('.jpeg')[0]+'.gray.bmp')
outfile=open(imagename.split('.jpeg')[0]+'.grayscale.true.txt','w')
for i in xrange(height):
	for j in xrange(width):
		outfile.write('%d '%(pix[j,i]))
	outfile.write('\n')
outfile.close()
