import re

# Corrected email regex pattern
extracted_email = re.compile(r"[a-zA-Z0-9\.+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}")
extracted_number = re.compile(r"\+{1}[0-9]{2} [0-9]{3} [0-9]{7}")

name_pattern = r'\b(?:name|candidate)\s*:\s*([a-z ]+)\b'


def extract_experience(text):
    experience_keywords = ["experience", "work experience", "positions held"]
    experiences = []

    for line in text.splitlines():
        if any(keyword in line.lower() for keyword in experience_keywords):
            # Found a potential experience line
            next_lines = []
            for i in range(1, 3):  # Capture 2 lines below the keyword line
                next_line_index = text.splitlines().index(line) + i
                if next_line_index < len(text.splitlines()):
                    next_lines.append(text.splitlines()[next_line_index])
            experience_text = "\n".join([line] + next_lines)
            experiences.append(experience_text)

    return experiences


# Read the text data from the file
file_path = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/extracted_data/extracted_data.txt"
with open(file_path, "r") as file:
    text_data = file.read()

# print(text_data)


print(extracted_email.search(text_data))
print(extracted_number.search(text_data))


extracted_experiences = extract_experience(text_data)
print("Extracted Experiences:",extracted_experiences)
for experience in extracted_experiences:
    print(experience,"name")