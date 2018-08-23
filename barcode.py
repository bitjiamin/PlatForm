from pyzbar.pyzbar import decode
from PIL import Image
import clr


a=decode(Image.open('C:/Project/Image/111.jpeg'))
print(a[0])
print(a[1])

