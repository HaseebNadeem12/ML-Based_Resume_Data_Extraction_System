import re
import json
import os
import requests


# Replace normalize_text function as needed
def normalize_text(text):
    text = text.lower()  # Convert to lowercase
    return text


# Function to extract text using OCR.space API
def extract_text_from_pdf_ocr_space(pdf_path, api_key):
    # URL for OCR.space API
    url = 'https://api.ocr.space/parse/image'

    with open(pdf_path, 'rb') as file:  # Line opens the PDF file in binary mode
        # Send POST request to the OCR API
        response = requests.post(
            url,
            files={'file': file},  # The key 'file' is used to indicate that this is the file being uploaded.
            data={  # The data parameter contains additional information for the API
                'apikey': api_key,
                'language': 'eng',  # Language of the document
                'isOverlayRequired': False  # No word overlays needed
            }
        )

    # Handle response
    if response.status_code == 200:  # status code is 200 (which means "OK" or "success").
        result = response.json()
        parsed_text = result.get("ParsedResults")[0].get("ParsedText")  # Get the extracted text from the response
        # Normalize and return the extracted text
        return normalize_text(parsed_text)
    else:
        print(f"Failed to extract text. Status Code: {response.status_code}")
        return None


# Function to extract text from file (replaces the old extract_text_from_pdf)
def extract_text_from_file(received_file, api_key):
    extension = os.path.splitext(received_file)[1].lower()  # Extract the file extension

    if extension == ".pdf":
        return extract_text_from_pdf_ocr_space(received_file, api_key)
    else:
        raise ValueError(f"Unsupported file type: {extension}")


# Example usage
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_cv09.pdf"
api_key = 'K84586442588957'  # Your OCR.space API key

extracted_text = extract_text_from_file(my_file, api_key)
# print(extracted_text)

# Create a directory for saving extracted data
directory_path = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/extracted_data"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Write text data to a file
file_path = os.path.join(directory_path, "extracted_data.txt")
with open(file_path, "w") as file:
    file.write(extracted_text)

# Define regex patterns for email and phone number
extracted_email = re.compile(r"[a-zA-Z0-9\.+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}")
extracted_number = re.compile(r"\+{1}[0-9]{2} [0-9]{3} [0-9]{7}")

# Define the experience pattern
experience_pattern = re.compile(
    r'(adult care experience|childcare experience|employment history)\s*'  # Matches section headers
    r'(.+?)(?=\n\s*\w)',  # Captures all text until the next section header
    re.IGNORECASE | re.DOTALL)

# Extract email and phone number
email = extracted_email.search(extracted_text)
phone = extracted_number.search(extracted_text)

# Find all experience sections
experience_sections = experience_pattern.findall(extracted_text)

# Initialize a dictionary to hold structured data
resume_data = {
    "personal_information": {
        "email": email.group() if email else None,
        "phone_number": phone.group() if phone else None
    },
    "experience": []
}

# Populate the experience sections
for section in experience_sections:
    header, content = section
    resume_data["experience"].append({
        "section": header.lower(),  # Store section headers in lowercase
        "details": content.strip()   # Store the content of the experience section
    })

# Convert the resume data to JSON format
json_file_path = os.path.join(directory_path, "extracted_data.json")
with open(json_file_path, "w") as json_file:
    json.dump(resume_data, json_file, indent=4)

print("Extracted data saved to JSON.")

# Print the entire structured JSON data in a readable format
print(json.dumps(resume_data, indent=4))
