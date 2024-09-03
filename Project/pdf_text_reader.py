from cgitb import reset

import pytesseract
import cv2
import os
import re
import numpy as np
from   pdf2image import convert_from_path
from   PyPDF2    import PdfReader

def normalize_text(text):
    text = text.lower()                              # Convert to lowercase
    # text = text.replace(" ","")                    # removing spaces
    # text = re.sub(r'[^\w\s]', '', text)            # Remove special characters using regex
    # text = ' '.join(text.split())                   # Remove extra whitespace
    return text

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:

            reader = PdfReader(file)  # Use PdfReader to read pdf
            text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

            if text.strip():
                text = normalize_text(text)
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

def extract_text_from_file(received_file):
    extension = os.path.splitext(received_file)[1].lower()

    if extension == ".pdf":
        pdf_text = extract_text_from_pdf(received_file)
        return pdf_text
    else:
        raise ValueError(f"Unsupported file type: {extension}")

# Example usage:
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_cv09.pdf"
extracted_text = extract_text_from_file(my_file)
# print(extracted_text)

# Create a directory
directory_path = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/extracted_data"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Write text data to a file
file_path = os.path.join(directory_path, "extracted_data.txt")
with open(file_path, "w") as file:
    file.write(extracted_text)

# for email and phone number
extracted_email = re.compile(r"[a-zA-Z0-9\.+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}")
extracted_number = re.compile(r"\+{1}[0-9]{2} [0-9]{3} [0-9]{7}")

# experience_pattern = re.compile(r'(?:experience|employment history)\s*:\s*(.+?)(?:education|$)')
experience_pattern = re.compile(
    r'(adult care experience|childcare experience|employment history)\s*'  # Matches section headers
    r'(.+?)(?=\n\s*\w)',  # Captures all text until the next section header
    re.IGNORECASE | re.DOTALL)

email = extracted_email.search(extracted_text)
print(email.group())
print(extracted_number.search(extracted_text))

# Find all experience sections
experience_sections = experience_pattern.findall(extracted_text)

for section in experience_sections:
    header, content = section
    print(f"{header.upper()}:")
    print(content.strip())
    print()

