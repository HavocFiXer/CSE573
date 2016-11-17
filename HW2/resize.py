from PIL import Image
import sys

im=Image.open(sys.argv[1])

pix=int(sys.argv[3])
newim=im.resize((pix,pix))

newim.save(sys.argv[2])
