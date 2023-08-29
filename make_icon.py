from PIL import Image
# filename = r'Picture1.png'
filename = r'pngegg.png'
img = Image.open(filename)
img.save('UTIL.ico', format = 'ICO', sizes = [(255,255)])