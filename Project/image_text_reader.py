import pytesseract
import cv2
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# Normalization of the text
def normalize_text(text):
    text = text.lower()                                          # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)              # Remove special characters using regex
    text = ' '.join(text.split())                                # Remove extra whitespace
    return text

# Function to extract text from an image or image path
def extract_text_from_image(image):

    if isinstance(image, str):
        # If a file path is provided, read the image
        image = cv2.imread(image)

    # Use pytesseract to extract text from the image
    reading_image_text = pytesseract.image_to_string(image)
    return normalize_text(reading_image_text)


# Function to handle both file paths and image arrays
def extract_text_from_file(received_file_or_image):
    if isinstance(received_file_or_image, str):
        # If a file path is provided, extract extension
        extension = os.path.splitext(received_file_or_image)[1].lower()

        if extension in [".png", ".jpg", ".jpeg", ".tiff"]:
            # If it's an image file, process it using extract_text_from_image
            return extract_text_from_image(received_file_or_image)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    elif isinstance(received_file_or_image, np.ndarray):
        # If an image array is provided directly, process it
        return extract_text_from_image(received_file_or_image)
    else:
        raise ValueError("Unsupported input type: expected a file path or an image array.")

# To display the image
def display(image):
    dpi = 100

    # If the input is a file path (string), load the image using plt.imread
    if isinstance(image, str):
        im_data = plt.imread(image)
    else:
        im_data = image

    # Get the dimensions of the image
    height, width = im_data.shape[:2]

    # Calculate figure size in inches
    figsize = width / float(dpi), height / float(dpi)

    # Create the figure and axis
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])  # Full image without padding
    ax.axis('off')  # Hide the axes
    ax.imshow(im_data, cmap='gray')  # Display the image
    plt.show()
    return im_data

def NoNoiseFunc(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(im_bw, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    # display(image)
    return image

img = cv2.imread("C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/my_doc_image03.jpg")
# my_file = "C:/Users/COMTECH COMPUTER/PycharmProjects/Optical_Character_Recognization01/Data01/News_image.png"

# Assigning to another variable (if needed for later use)
get_image1 = display(img)
get_image2 = NoNoiseFunc(get_image1)
extracted_text = extract_text_from_image(get_image2)

print(extracted_text)

