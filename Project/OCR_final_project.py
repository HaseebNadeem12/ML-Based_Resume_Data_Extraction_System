import pytesseract
import cv2
import os
import textract
from   pdf2image import convert_from_path
from   PyPDF2    import PdfReader
from   docx      import Document
import numpy as np


def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:

            reader = PdfReader(file)  # Use PdfReader to read pdf
            text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

            if text.strip():
                text = text.lower()
                return text

    except Exception as e:
        print(f"Direct extraction failed: {e}")

    # If direct extraction fails or no text is found, use OCR
    images = convert_from_path(pdf_path)
    text = ""

    for image in images:
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        text += pytesseract.image_to_string(open_cv_image)

    return text


def extract_text_from_docx(docx_path):

    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    text = text.lower()

    if docx_path == ".doc":

        try:
            text_1 = textract.process(docx_path).decode('utf-8')
            text_1 = text_1.lower()
            return text_1

        except Exception as e:
            print(f"Failed to extract text from .doc file using textract: {e}")
            return ""

    else:
        return text


def extracted_text_from_images(input_image):
    # Check if the image path is correct and the file can be loaded
    if isinstance(input_image, str):
        my_image = cv2.imread(input_image)

        # Check if the image was loaded successfully
        if my_image is None:
            raise FileNotFoundError(f"Image not found or could not be loaded: {input_image}")

        # 1. convert image to gray image
        gray_image_pyte = cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY)

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

        # -> to get the row result separately, initializing counter
        roi_counter = 0
        result = []

        # -> For creating rectangle box on original image(to select the colomns)
        for count in contour_image:

            x, y, w, h = cv2.boundingRect(count)
            # -> condition to get rio from overlaping of selected area(contours)
            if h > 200 and w > 20:

                # -> to capture bounding boxes
                roi = my_image[y:y + h, x:x + w]  # -> return last column
                cv2.rectangle(my_image, (x, y), (x + w, y + h), (36, 255, 12), 2)

                # storing column if any
                roi_filename = ("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_{}.JPG").format(roi_counter)
                cv2.imwrite(roi_filename, roi)
                roi_counter += 1

                # -> To read the text of that individual colomns
                text_of_roi_01 = pytesseract.image_to_string("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Pytesseract/roi_image_0.JPG")

                # -> Processing steps for better output
                text_of_roi_01 = text_of_roi_01.split("\n")

                for item in text_of_roi_01:
                    result.append(item)

        # -> For further process the text to get desired text
        all_entities = []

        for item in result:

            if len(item) >= 4 and isinstance(item, str):

                item.replace('\n', "")
                all_entities.append(item)
                print(item)


def extract_text_from_file(received_file):
    extension = os.path.splitext(received_file)[1].lower()

    if extension == ".pdf":
        print("pdf")
        pdf_text = extract_text_from_pdf(received_file)
        return pdf_text

    elif extension in ".doc , .docx":
        print("word")
        word_text = extract_text_from_docx(received_file)
        return word_text

    elif extension in ".png,.jpg,.jpeg,.tiff":
        image_text = extracted_text_from_images(received_file)
        return image_text

    else:
        raise ValueError(f"Unsupported file type: {extension}")

# Example usage:
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_cv09.pdf"
extracted_text = extract_text_from_file(my_file)
print(extracted_text)

