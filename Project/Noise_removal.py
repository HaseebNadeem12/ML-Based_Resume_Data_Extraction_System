"""for No noise image"""
# Important steps
# 1-read image with CV2
# 2-Binarization
#   -convert image to gray image(one colour image)
#   -convert image to theshold level(white text, black background)
# 3-Noise Removal
#   -convert to kernal
#   -dialate the image
#   -erode the image
#   -morpholize the image
#   -blur the image

import cv2
import numpy as np
import matplotlib.pyplot as plt

def display(image):
    dpi = 100

    # If the input is a file path (string), load the image using plt.imread
    if isinstance(image, str):
        im_data = plt.imread(image)
    else:
        im_data = image

    # Get the dimensions of the image
    height, width = im_data.shape[:2]

    # Calculate figure size in inches
    figsize = width / float(dpi), height / float(dpi)

    # Create the figure and axis
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])  # Full image without padding
    ax.axis('off')  # Hide the axes
    ax.imshow(im_data, cmap='gray')  # Display the image
    plt.show()
    return im_data

# display(img)

def NoNoiseFunc(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(im_bw, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    # display(image)
    return image


img = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_01.jpg")
get_image1 = NoNoiseFunc(img)
get_image2 = display(get_image1)


