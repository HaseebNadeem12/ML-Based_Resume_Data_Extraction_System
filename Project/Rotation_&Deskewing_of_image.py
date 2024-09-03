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

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, threshold, kernal, and dialate
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    for c in contours:
        rect = cv2.boundingRect(c)
        #->Gets the bounding box (rectangle) around each contour
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)
        #->Draws a green rectangle around each contour, primarily for visualization.

    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("OpenCV/boxes.jpg", newImage)
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    #->Extracts the height and width of the image.
    center = (w // 2, h // 2)
    #->Determines the center point of the image, which will be the pivot for rotation.
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image after getting skew angle and knowing the mid point of the image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

new_image = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/Image_03(Rotated).JPG")
fixed = deskew(new_image)
cv2.imwrite("OpenCV/rotated_fixed.jpg", fixed)

display(fixed)

