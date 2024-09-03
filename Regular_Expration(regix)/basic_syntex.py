import re

# my_pattern = re.compile(r"^[a-zA-Z]$")
# # It matches only single capital or lower case letter
# print(my_pattern.seach("a"))

# # 3 lower case latter
# # 2 upper case letter
# # 1 special case
# # 3 numbers
# my_pattern1 = re.compile(r"[a-z]{3}[A-Z]{2}[^a-zA-Z0-9]{1}[0-9]{3}")
# print(my_pattern1.search("abbHM@123"))
# #-> It matches the above password

# my_pattern2 = re.compile(r"^[a-zA-Z]{6,15}[0-9]{3,5}@{1}[a-zA-Z0-9\-]{4,6}\.[a-zA-Z]{2,6}$")
# print(my_pattern2.search("haseebnadeem882@gmail.com"))
# # matches the email id

# my_pattern3 = re.compile(r"^[0-9]{3}\-{1}[0-9]{3} [0-9]{4}$")
# it will match 012-345 6789 exactly the given format
# # it will match 012-345 6789 exactly the given format
# print(my_pattern3.search("123-326 8764"))    #->matches
# print(my_pattern3.search("341-247 9887"))    #->matches
# print(my_pattern3.search("123-326 874"))     #->not match

# my_pattern3 = re.compile(r"^[0-9]{3}\-{1}[0-9]{3} [0-9]{4}$")
# matches01 = my_pattern3.match("111-234 2345")    # matche the pattern with certain input, email or perticular string
# # search01 = my_pattern3.search("111-234 2345")   # search the given pattern in the text
#
# print(matches01,type(matches01))
#
# if matches01:
#     print("text contains the given pattern")
# else:
#     print("not found")

# import re

import re

def extract_experience(resume_text):
    """Extracts experience information from a resume text.

    Args:
        resume_text (str): The text content of the resume.

    Returns:
        list: A list of dictionaries, each representing an experience entry with
            'company', 'title', 'start_date', 'end_date' keys.
    """

    # experience_pattern = r"(?P<company>[A-Za-z\s]+)\s+(?P<title>[A-Za-z\s]+) \s+\( (?P<start_date>\d{4}-\d{2}-\d{2}) \s+-\s+ (?P<end_date>\d{4}-\d{2}-\d{2}) )\s+.*"
    experience_pattern = r"(?P<company>[A-Za-z\s]+)\s+"


    matches = re.findall(experience_pattern, resume_text)

    experiences = []
    for match in matches:
        company, title, start_date, end_date = match
        experiences.append({
            "company": company,
            "title": title,
            "start_date": start_date,
            "end_date": end_date
        })

    return experiences

# Example usage:
resume_text = "Worked at XYZ Company as a Software Engineer from 2015-2020. Led a team of 5 developers."

extracted_experiences = extract_experience(resume_text)
print(extracted_experiences)
















