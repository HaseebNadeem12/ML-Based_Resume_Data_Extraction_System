
import cv2
from PIL import Image
import pytesseract
from PIL.IcnsImagePlugin import read_png_or_jpeg2000

#importing image into memory(in the form of series of numerical array)
#for imorting images into memory we always use pillow for this
im_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_02.jpg"

#Basic operation to see image
im = Image.open(im_file)
print(im.size)
im.show()
# Rotate the image
im.rotate(180).show( )

#save image into different directory
#I give full file path
im.save("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pillow_Library01/image_02.jpg")





