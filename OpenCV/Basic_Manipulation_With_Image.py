"""0. Opening an Image"""
import cv2
import matplotlib.pyplot as plt

# Load the image using OpenCV
image_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_01.jpg"
img = cv2.imread(image_file)

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

# Display the original image
display(img)



"""1. Inverted Images"""
# #-> turns white colour into black and vise versa
# inverted_image = cv2.bitwise_not(img)
# cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/OpenCV/inverted_01.jpg", inverted_image)
#
# # Display the inverted image
# display(inverted_image)
# # plt.imshow
# # plt.show()

"""2. Recycling"""


"""3. Binarization"""
# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/OpenCV/gray_image.jpg", gray_image)
#
# # Display the grayscale image using the image array
# display(gray_image)
#
# thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
# cv2.imwrite("OpenCV/bitwise_image.jpg", im_bw)
# display(im_bw)
# # display(thresh) #-> Why not able to display


"""4. Noise Removal"""
# def noise_removal(image):
#     import numpy as np
#     kernel = np.ones((1, 1), np.uint8)
#     # 'np.uint8' specifies that the values are 8-bit unsigned integers, which is standard for image data.
#     image = cv2.dilate(image, kernel, iterations=1)
#     # Dilation helps to close small holes within the foreground objects, which can help reduce noise.
#     # kernel = np.ones((1, 1), np.uint8)
#     image = cv2.erode(image, kernel, iterations=1)
#     # Erosion is applied after dilation. This step helps to remove any small white noise remaining
#     # after dilation by eroding away the outer layers of the objects.
#     image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
#     # Crutial step after dialation and erosion
#     # This function applies the morphological closing operation using the same kernel.
#     # It is effective for removing small black points on the white object.
#     image = cv2.medianBlur(image, 3)
#     # It replace each pixel’s value with the median of the neighboring pixel values.
#     # cv2.medianBlur(image, 3): This function applies a median blur to the image with a kernel size of 3x3.
#     # This helps to further reduce noise while preserving edges.
#     return (image)
#
# no_noise = noise_removal(im_bw)
# cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/OpenCV/no_noise.jpg", no_noise)
#
# display(no_noise)

"""5. Dilation and Erosion"""
# # This is particularly useful in images where the text is bold or closely packed,
# # Dilation: Expands the boundaries (also used of objects to close small holes and connect nearby objects).
# # Erosion: Shrinks the object boundaries (also used to remove small noise and separate connected objects.)
# def thin_font(image):
#     import numpy as np
#     image = cv2.bitwise_not(image)
#     # This function inverts the pixel values of the image, converting black to white and white to black.
#     # erosion operation in OpenCV works by expanding the dark (black) regions
#     kernel = np.ones((2,2),np.uint8)
#     image = cv2.erode(image, kernel, iterations=1)
#     image = cv2.bitwise_not(image)
#     return (image)
#
# eroded_image = thin_font(no_noise)
# cv2.imwrite("OpenCV/eroded_image.jpg", eroded_image)
#
# display(eroded_image)
#
# def thick_font(image):
#     import numpy as np
#     image = cv2.bitwise_not(image)
#     kernel = np.ones((2,2),np.uint8)
#     image = cv2.dilate(image, kernel, iterations=1)
#     # Opposite of errosion
#     image = cv2.bitwise_not(image)
#     return (image)
#
# dilated_image = thick_font(no_noise)
# cv2.imwrite("OpenCV/dilated_image.jpg", dilated_image)
#
# display(dilated_image)

"""6. Rotation / Deskewing"""
new_image = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/Image_03(Rotated).JPG")
# display(new_image)

#https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
import numpy as np

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    #->Converts the image to grayscale, which simplifies processing by reducing the color channels to one.
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    #->Applies Gaussian Blur to the grayscale image to reduce noise and detail, which helps in more accurate thresholding.
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #-> Applies Otsu's thresholding to convert the image to a binary image (black and white).
    #-> 'cv2.THRESH_BINARY_INV flag inverts the image, making text white and the background black.


    # Apply dilate to merge text into meaningful lines/paragraphs.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    #-> The large width of the kernel helps in merging text characters into single lines by canceling out spaces
    dilate = cv2.dilate(thresh, kernel, iterations=2)
    #->Applies dilation to the thresholded image, merging characters into lines or blocks, making it easier to identify the skew angle.

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #->Finds contours in the dilated image. Contours are curves joining all the continuous points along a boundary that have the same color or intensity.
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    #->Sorts the contours by area, in descending order, so that the largest contour (likely the text block) is processed first.

    for c in contours:
        rect = cv2.boundingRect(c)
        #->Gets the bounding box (rectangle) around each contour
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)
        #->Draws a green rectangle around each contour, primarily for visualization.

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    #->'contours[0]: Selects the largest contour
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    #->Finds the minimum area rectangle that can enclose the largest contour.
    #->This rectangle may be rotated, which helps determine the skew angle.
    cv2.imwrite("OpenCV/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    # ->The last value in minAreaRect is the angle of rotation.
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

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new_image)
# print(fixed)
cv2.imwrite("OpenCV/rotated_fixed.jpg", fixed)

display(fixed)

"""7.Removing Borders """
# # Using picture with boarder
# # display(no_noise)
#
# def remove_borders(image):
#     contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     #->cv2.findContours(): This function detects the contours in the image.
#     #->Contours: Contours are curves joining all the continuous points along a boundary with the same color or intensity.
#     # In this case, they help identify the borders of the image.
#     cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
#     cnt = cntsSorted[-1]
#     x, y, w, h = cv2.boundingRect(cnt)
#     crop = image[y:y+h, x:x+w]
#     #->image[y:y+h, x:x+w]: This slicing operation extracts the part of the image inside the bounding rectangle
#     return (crop)
#
# no_borders = remove_borders(no_noise)
# cv2.imwrite("OpenCV/no_borders.jpg", no_borders)
# display(no_borders)

"""8. Missing Borders"""
# # Using no boarder image, that we imported first
# color = [255, 255, 255]
# top, bottom, left, right = [150]*4
#
# image_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
# cv2.imwrite("OpenCV/image_with_border.jpg", image_with_border)
# display(img)
# display(image_with_border)

