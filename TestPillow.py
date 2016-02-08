from PIL import Image

f=open("test2.jpg",'w')
im = Image.new( 'RGB', (255,255), (128,128,128))
im.save(f, "JPEG")
f.close()
