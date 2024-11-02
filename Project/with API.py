import re
import json
import os
import nltk
import requests


# Replace normalize_text function as needed
def text_preprocessing(text):
    text = text.lower()

    return text

# Function to extract text using OCR.space API
def extract_text_from_pdf_ocr_space(pdf_path, api_key):
    url = 'https://api.ocr.space/parse/image'

    with open(pdf_path, 'rb') as file:
        # Send POST request with a timeout of 30 seconds
        try:
            response = requests.post(
                url,
                files={'file': file},
                data={
                    'apikey': api_key,
                    'language': 'eng',
                    'isOverlayRequired': False
                },
                timeout=30  # Timeout in seconds
            )

            if response.status_code == 200:
                result = response.json()
                parsed_text = result.get("ParsedResults")[0].get("ParsedText")
                return text_preprocessing(parsed_text)
            else:
                print(f"Failed to extract text. Status Code: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print("The request timed out. Please try again.")
            return None

# Function to extract text from file
def extract_text_from_file(received_file, api_key):
    extension = os.path.splitext(received_file)[1].lower()
    if extension != ".pdf":
        return extract_text_from_pdf_ocr_space(received_file, api_key)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

# File path and API key
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/image_01.jpg"
api_key = 'K89435865588957'

extracted_text = extract_text_from_file(my_file, api_key)

if extracted_text:
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

    # Define patterns for various sections
    experience_pattern  = re.compile(r'(experience|work experience|employment history)\s*(.+?)(?=\n\s*\w)', re.IGNORECASE | re.DOTALL)
    education_pattern   = re.compile(r'(education|academic background|qualifications)\s*(.+?)(?=\n\s*\w)', re.IGNORECASE | re.DOTALL)
    skill_pattern       = re.compile(r'(skills|technical skills|core competencies|soft skills|hard skills)\s*:\s*(.+?)(?=\n\s*\w|\Z)', re.IGNORECASE | re.DOTALL)
    certificate_pattern = re.compile(r'(certificate|certifications|courses)\s*(.+?)(?=\n\s*\w)')

    # Extract Information
    email = extracted_email.search(extracted_text)
    phone = extracted_number.search(extracted_text)

    experience_sections = experience_pattern.findall(extracted_text)
    education_section = education_pattern.findall(extracted_text)
    skill_section = skill_pattern.findall(extracted_text)
    certificate_section = certificate_pattern.findall(extracted_text)

    # Initialize a dictionary to hold structured data
    resume_data = {
        "personal_information": {
            "email": email.group() if email else None,
            "phone_number": phone.group() if phone else None
        },
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": []  # Fixed the typo to match JSON schema ("certifications")
    }

    # Populate the experience sections
    for section in experience_sections:
        header, content = section
        resume_data["experience"].append({
            "section": header.lower(),
            "details": content.strip()
        })

    # Populate the education sections
    for section in education_section:
        header_1, content_1 = section
        resume_data['education'].append({
            "section": header_1.lower(),
            "details": content_1.strip()
        })

    # Populate the skills sections
    for section in skill_section:
        header_3, content_3 = section
        resume_data['skills'].append({
            "section": header_3.lower(),
            "details": content_3.strip()
        })

    # Populate the certificate sections
    for section in certificate_section:
        header_4, content_4 = section
        resume_data['certifications'].append({
            "section": header_4.lower(),
            "details": content_4.strip()  # Corrected content reference
        })

    # Convert the resume data to JSON format and save it
    json_file_path = os.path.join(directory_path, "extracted_data.json")
    with open(json_file_path, "w") as json_file:
        json.dump(resume_data, json_file, indent=4)

    print("Extracted data saved to JSON.")
    # Print the structured JSON data
    print(json.dumps(resume_data, indent=4))

else:
    print("No text was extracted.")