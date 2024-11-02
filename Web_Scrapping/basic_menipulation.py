import requests

# # Make a GET request to a URL
# response = requests.get('https://api.github.com')
#
# # Print the status code of the response
# print(response.status_code)  # 200 means the request was successful
#
# # Print the content of the response
# print(response.text)  # Shows the raw HTML or JSON content


"""Using Request"""
# import requests
#
# def scrape_amazon_reviews_requests(url):
#     response = requests.get(url)
#     text = response.text
#     # Parse the text using a suitable HTML parser (e.g., Beautiful Soup, lxml)
#     # ...
#
# # Replace 'your_product_url' with the actual URL of the product
# scrape_amazon_reviews_requests('https://www.amazon.com/your_product_url')


"""Using Beautiful Soup"""
import requests
from bs4 import BeautifulSoup

def scrape_amazon_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = soup.find_all('div', class_='review-text')
    for review in reviews:
        review_text = review.text
        # Extract other relevant information (e.g., rating, date)
        print(review_text)

# Replace 'your_product_url' with the actual URL of the product
scrape_amazon_reviews('https://www.amazon.com/your_product_url')


"""Using Selenium"""
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# def scrape_amazon_reviews_selenium(url):
#     driver = webdriver.Chrome()  # Replace 'Chrome' with the path to your WebDriver
#     driver.get(url)
#
#     reviews = driver.find_elements(By.CSS_SELECTOR, '.review-text')
#     for review in reviews:
#         review_text = review.text
#         # Extract other relevant information (e.g., rating, date)
#         print(review_text)
#
#     driver.quit()
#
# # Replace 'your_product_url' with the actual URL of the product
# scrape_amazon_reviews_selenium('https://www.amazon.com/your_product_url')



