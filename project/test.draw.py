import sys
import numpy as np
import cPickle as cp
import scipy.signal
import os
#from skimage import filter
import skimage.filter
#from feature import canny
from PIL import Image, ImageFilter, ImageDraw

imagename=sys.argv[1]
drawim=Image.open(imagename)
draw=ImageDraw.Draw(drawim)
draw.line((20,30, 50, 50), fill='red')
draw.ellipse((20,30,50,50),fill=None, outline='blue')
drawim.save(imagename.split('.jpg')[0]+'.circles.jpg')
