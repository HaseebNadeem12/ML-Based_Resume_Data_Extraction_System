import re
import json
import os
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report

from Project.pdf_text_reader import email


# Function to normalize text
def normalize_text(text):
    text = text.lower()  # Convert to lowercase
    return text

# Function to extract text using OCR.space API
def extract_text_from_pdf_ocr_space(pdf_path, api_key):
    url = 'https://api.ocr.space/parse/image'

    with open(pdf_path, 'rb') as file:  # Open the PDF file in binary mode
        response = requests.post(
            url,
            files={'file': file},
            data={
                'apikey': api_key,
                'language': 'eng',
                'isOverlayRequired': False
            }
        )

    if response.status_code == 200:
        result = response.json()
        parsed_text = result.get("ParsedResults")[0].get("ParsedText")
        return normalize_text(parsed_text)
    else:
        print(f"Failed to extract text. Status Code: {response.status_code}")
        return None

# Function to extract text from file
def extract_text_from_file(received_file, api_key):

    # Seperate out name and extension and store extenstion
    extension = os.path.splitext(received_file)[1].lower()

    if extension == ".pdf" or ".docx" or ".doc":
        return_text = extract_text_from_pdf_ocr_space(received_file, api_key)
        return return_text

    else:
        raise ValueError(f"Unsupported file type: {extension}")


# File path and API key
my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_cv_imp01.pdf"
api_key = 'K84586442588957'

extracted_text = extract_text_from_file(my_file, api_key)


# Create a directory for saving extracted data
directory_path = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/extracted_data"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Write text data to a file
file_path = os.path.join(directory_path, "extracted_data.txt")
with open(file_path, "w") as file:
    file.write(extracted_text)


# Define regex patterns for email, phone number
extracted_email = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
extracted_number = re.compile(r"\+?[0-9]{1,3}[-.\s]?[0-9]{3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{4}")

# Extracting information for each section
experience_pattern  = re.compile(r'(experience|work experience|employment history)\s*([\s\S]+?)(?=(education|skills|certifications|\Z))', re.IGNORECASE)
education_pattern   = re.compile(r'(education|academic background|qualifications)\s*([\s\S]+?)(?=(experience|skills|certifications|\Z))', re.IGNORECASE)
skill_pattern       = re.compile(r'(skills|technical skills|core competencies|soft skills|hard skills)\s*([\s\S]+?)(?=(experience|education|certifications|\Z))', re.IGNORECASE)
certificate_pattern = re.compile(r'(certificate|certifications|courses)\s*([\s\S]+?)(?=(experience|education|skills|\Z))', re.IGNORECASE)


# Extracting Information
email = extracted_email.search(extracted_text)
phone = extracted_number.search(extracted_text)

experience_sections  = experience_pattern.findall(extracted_text)
education_sections   = education_pattern.findall(extracted_text)
skill_sections       = skill_pattern.findall(extracted_text)
certificate_sections = certificate_pattern.findall(extracted_text)

# Initialize a dictionary to hold structured data
resume_data = \
{
    "personal_information":
    {
        #condition to check email and phone number
        "email": email.group() if email else None,
        "phone_number": phone.group() if phone else None
    },

    "experience": [],
    "education": [],
    "skills": [],
    "certifications": []
}

print(experience_sections)

# Collecting the experience information
for section in experience_sections:
    header, content,null = section
    resume_data["experience"].append({
        "section": header.lower(),
        "details": content.strip()
    })

# Collecting the education information
for section in education_sections:
    header, content, null = section
    resume_data["education"].append({
        "section": header.lower(),
        "details": content.strip()
    })

# Collecting the skill information
for section in skill_sections:
    header, content, null = section
    resume_data["skills"].append({
        "section": header.lower(),
        "details": content.strip()
    })

# Collecting the certificate information
for section in certificate_sections:
    header, content, null = section
    resume_data["certifications"].append({
        "section": header.lower(),
        "details": content.strip()
    })

# Convert the resume data to JSON format and save it
json_file_path = os.path.join(directory_path, "extracted_data.json")
with open(json_file_path, "w") as json_file:
    json.dump(resume_data, json_file, indent=4)

# Print the structured JSON data
print(json.dumps(resume_data, indent=4))


# Data for training SVM model
data = pd.read_csv("C:/Users/COMTECH COMPUTER/Desktop/Data_for_training.csv")
data = data.dropna(subset=["Text"])

df = pd.DataFrame(data, columns=["Text", "Label"])

# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Text"])  # Convert text to numerical features
y = df["Label"]  # Labels (experience, education, etc.)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Support Vector Machine (SVM) model
model = SVC(kernel="linear")
model.fit(X_train, y_train)

# Test the model and evaluate performance
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Example: Classifying new sections
new_sections = ["certified java developer", "work experience with databases"]
new_X = vectorizer.transform(new_sections)
predictions = model.predict(new_X)
print(predictions)