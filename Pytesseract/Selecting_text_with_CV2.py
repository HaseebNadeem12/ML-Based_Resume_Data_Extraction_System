import pytesseract
import cv2
from numpy.ma.core import count

image_with_cv2 = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_05(With Colomns).JPG")
# Assigning to another variable (if needed for later use)
Copy_image = image_with_cv2
# print(image_with_cv2)

"""Preprocessing Steps"""
# 1. convert image to gray image
gray_image_pyte = cv2.cvtColor(image_with_cv2, cv2.COLOR_BGR2GRAY)
cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/gray_image.JPG",gray_image_pyte)

# 2. Blur image
blur_image = cv2.GaussianBlur(gray_image_pyte,(7,7),0)
cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/Blur_image.JPG",blur_image)

# 3. Threshold image(Converting into black and white)
threshold_image = cv2.threshold(blur_image,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/threshold_image.JPG",threshold_image)

# 4. Kernal the image
kernal_image = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/kernal_image.JPG",kernal_image)

# 5. Dialting the image
dialate_image = cv2.dilate(threshold_image,kernal_image,iterations=1)
cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/dialate_image.JPG",dialate_image)

# 6. Making contours of that dialted image
contour_image = cv2.findContours(dialate_image,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contour_image = contour_image[0] if len(contour_image) == 2 else contour_image[1]
contour_image = sorted(contour_image, key= lambda x: cv2.boundingRect(x)[0])

#-> to get the roi result seprately, initializing counter
roi_counter = 0

result = []

#-> For creating rectangle box on original image(to select the colomns)
for count in contour_image:
    x, y, w, h = cv2.boundingRect(count)

    #-> condition to get rid from overlaping of selected area(contours)
    if h > 200 and w > 20 :

        #-> to capture individual bounding boses
        roi = image_with_cv2[y:y+h , x:x+w]  #-> return last coloumn
        cv2.rectangle(image_with_cv2, (x, y), (x + w, y + h), (36, 255, 12), 2)

        # storing individual column
        roi_filename = ("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_{}.JPG").format(roi_counter)
        cv2.imwrite(roi_filename, roi)
        roi_counter += 1

        #-> To read the text of that individual colomns
        text_of_roi_01 = pytesseract.image_to_string("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_0.JPG")
        # print(text_of_roi_01)

        #-> Processing steps for better output
        text_of_roi_01 = text_of_roi_01.split("\n")
        for item in text_of_roi_01:
            result.append(item)

cv2.imwrite("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/contour_image.JPG",image_with_cv2)
# print(result)

#-> For further process the text to get desired text
all_entities = []
for item in result:
    item = item.strip()
    item = item.split(" ")[0]
    if len(item) > 2 :
        if item[0].isupper() and "-" not in item:
            # print(item)
            item = item.split(".")[0].replace(",","")
            all_entities.append(item)
            # print(item)

# to remove all similar entities
all_entities = list(set(all_entities))
print(all_entities)



