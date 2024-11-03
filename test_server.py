import requests

print(requests.get('http://127.0.0.1:8000/quest-items').json())

url = "http://127.0.0.1:8000/upload-image/0/1"
#image_path = "test_post_images/3ffdb298-383a-425e-8dc4-e7808233be45 - Copy.jpg"
image_path = "test_post_images/brdgebristol.jpeg"

# Open the image file in binary mode and send it
with open(image_path, 'rb') as image_file:
    files = {'file': image_file}
    response = requests.post(url, files=files)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())

