import pytesseract
import cv2
import os
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from docx import Document
import textract


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    text = text.lower()
    return text

def extract_text_from_doc(doc_path):
    try:
        text_1 = textract.process(doc_path).decode('utf-8')
        text_1 = text_1.lower()
        return text_1

    except Exception as e:
        print(f"Failed to extract text from .doc file using textract: {e}")
        return ""

def extract_text_from_file(received_file):
    extension = os.path.splitext(received_file)[1].lower()

    if extension == ".docx":
         result = extract_text_from_docx(received_file)
         return result

    elif extension == ".doc":
        result = extract_text_from_doc(received_file)
        return result

    else:
        raise ValueError(f"Unsupported file type: {extension}")

# Example usage:
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_cv03.docx"
extracted_text = extract_text_from_file(my_file)
print(extracted_text)


