from PIL import Image

im=Image.new('L',(2,2),0)
pix=im.load()
pix[0,0]=255
pix[0,1]=-1
pix[1,0]=255
pix[1,1]=255
im.save('make.bmp')
