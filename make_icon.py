from PIL import Image
filename = r'Picture1.png'
img = Image.open(filename)
img.save('MSL2.ico', format = 'ICO', sizes = [(255,255)])