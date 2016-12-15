import sys
import numpy as np
import cPickle as cp
import scipy.signal
from PIL import Image

imagename=sys.argv[1]
gaussian=np.array([	[1.0/16.0, 1.0/8.0, 1.0/16.0],
					[ 1.0/8.0, 1.0/4.0,  1.0/8.0],
					[1.0/16.0, 1.0/8.0, 1.0/16.0]])
im=Image.open(imagename).convert('L')
im.save(imagename.split('.jpg')[0]+'.black.jpg')
npim=np.array(im)
npdenoise=scipy.signal.convolve2d(npim, gaussian, mode='same')
height=npdenoise.shape[0]
width=npdenoise.shape[1]
Image.fromarray(np.uint8(npdenoise)).save(imagename.split('.jpg')[0]+'.gaussian.jpg')

