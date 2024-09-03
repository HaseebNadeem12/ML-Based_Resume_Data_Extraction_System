"""0. Opening an Image"""
import cv2
import matplotlib.pyplot as plt
# from six.moves import _thread
# import numpy as np
image_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_01.jpg"
img = cv2.imread(image_file)

plt.imshow(img)
plt.title('Original Image')
plt.show()

