import pytesseract
import cv2
import matplotlib.pyplot as plt

image_with_cv2 = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/Image_03(Rotated).JPG")
# Assigning to another variable (if needed for later use)

Copy_image = image_with_cv2
# print(image_with_cv2)


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
    final_image = ax.imshow(im_data, cmap='gray')  # Display the image
    # final_image.imshow(im_data, cmap = 'gray' )
    plt.show()
    return final_image



def pre_processed_text(imgage):
    # 1. convert image to gray image
    gray_image_pyte = cv2.cvtColor(imgage, cv2.COLOR_BGR2GRAY)

    # 2. Blur image
    blur_image = cv2.GaussianBlur(gray_image_pyte, (7, 7), 0)

    # 3. Threshold image(Converting into black and white)
    threshold_image = cv2.threshold(blur_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 4. Kernal the image(dividing image into rows)
    kernal_image = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

    # 5. Dialting the image
    dialate_image = cv2.dilate(threshold_image, kernal_image, iterations=1)

    # 6. Making contours of that dialated image(boxes on the entire image)
    contour_image = cv2.findContours(dialate_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_image = contour_image[0] if len(contour_image) == 2 else contour_image[1]
    contour_image = sorted(contour_image, key=lambda x: cv2.boundingRect(x)[0])

    return contour_image

def getSkewAngle(copy_image) -> float:

    newImage = copy_image.copy()

    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)


    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

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
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)


image_angle = deskew(image_with_cv2)
image_output = display(image_angle)
image_text = pre_processed_text(image_with_cv2)
print(image_text)


# #-> to get the row result separately, initializing counter
# roi_counter = 0
#
# result = []
# #-> For creating rectangle box on original image(to select the colomns)
# for count in image_text:
#     x, y, w, h = cv2.boundingRect(count)
#
#     #-> condition to get rio from overlaping of selected area(contours)
#     if h > 200 and w > 20 :
#
#         #-> to capture individual bounding boxes
#         roi = image_with_cv2[y:y+h , x:x+w]  #-> return last column
#         cv2.rectangle(image_with_cv2, (x, y), (x + w, y + h), (36, 255, 12), 2)
#
#         # storing individual column
#         roi_filename = ("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_{}.JPG").format(roi_counter)
#         cv2.imwrite(roi_filename, roi)
#         roi_counter += 1
#
#         #-> To read the text of that individual colomns
#         text_of_roi_01 = pytesseract.image_to_string("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_0.JPG")
#         # print(text_of_roi_01)
#
#         #-> Processing steps for better output
#         text_of_roi_01 = text_of_roi_01.split("\n")
#         for item in text_of_roi_01:
#             result.append(item)
# cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/contour_image.JPG",image_with_cv2)
# print(result)
#
# #-> For further process the text to get desired text
# all_entities = []
#
# for item in result:
#
#     if len(item) >= 4 and isinstance(item, str):
#
#         item.replace('\n',"")
#         all_entities.append(item)
#
#         print(item)
#
# print(all_entities)



