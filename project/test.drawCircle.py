import sys
import cPickle as cp
from PIL import Image

radius=int(sys.argv[1])
newim=Image.new('L',(512, 512), 0)
