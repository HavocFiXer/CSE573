import sys
import os

imagename=sys.argv[1]
infile=open(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.stat.txt')
outfile=open(imagename.split('.jpg')[0]+'/'+imagename.split('.jpg')[0]+'.max.txt','w')
for line in infile:
	rad=line.split('=>')[0]
	number=line.split('->')[1].split(':')[0]
	outfile.write('%s\n'%(number))
infile.close()
outfile.close()

