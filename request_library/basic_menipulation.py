import requests

# Make a GET request to a URL
response = requests.get('https://api.github.com')

# Print the status code of the response
print(response.status_code)  # 200 means the request was successful

# Print the content of the response
print(response.text)  # Shows the raw HTML or JSON content
