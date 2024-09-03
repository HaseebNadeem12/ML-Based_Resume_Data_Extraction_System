import pytesseract
import cv2
from pdf2image import convert_from_path
import PyPDF2
import textract
import os
from docx import Document
import numpy as np


# def extract_text_from_pdf(pdf_path):
#     # Try direct text extraction first
#     try:
#         with open(pdf_path, "rb") as file:
#             reader = PyPDF2.PdfFileReader(file)
#             text = ""
#             for page_num in range(reader.getNumPages()):
#                 page = reader.getPage(page_num)
#                 text += page.extract_text()
#             if text.strip():  # If text is extracted, return it
#                 return text
#     except Exception as e:
#         print(f"Direct extraction failed: {e}")
#
#     # If direct extraction fails or no text is found, use OCR
#     images = convert_from_path(pdf_path)
#     text = ""
#     for image in images:
#         open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#         text += pytesseract.image_to_string(open_cv_image)
#     return text


# def extract_text_from_image(image_path):
#     image = cv2.imread(image_path)
#     reading_image_text = pytesseract.image_to_string(image)
#     return reading_image_text


# def extract_text_from_docx(docx_path):
#     doc = Document(docx_path)
#     text = "\n".join([para.text for para in doc.paragraphs])
#     return text


def extract_text_from_doc(doc_path):
    return textract.process(doc_path).decode('utf-8')


def extract_text_from_file(recieved_file):

    extension = os.path.splitext(recieved_file)[1].lower()

    # if extension == ".pdf":
    #     pdf_text = extract_text_from_pdf(recieved_file)
    #     return pdf_text

    # if extension in [".png", ".jpg", ".jpeg", ".tiff"]:
    #     image_text = extract_text_from_image(recieved_file)
    #     return image_text
    # if extension == ".docx":
    #     return extract_text_from_docx(recieved_file)
    elif extension == ".doc":
        return extract_text_from_doc(recieved_file)
    else:
        raise ValueError(f"Unsupported file type: {extension}")


# Example usage:
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/News_image.png"
extracted_text = extract_text_from_file(my_file)
print(extracted_text)
