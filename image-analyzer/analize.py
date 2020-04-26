import requests
import json
from draw import *

# REST API call from Python
SUBSCRIPTION_KEY = "8970c5afe19b44a3bfb91581212a83dc"
vision_service_address = "https://francecentral.api.cognitive.microsoft.com/vision/v2.0/"
address = vision_service_address + "analyze"

parameters  = {'visualFeatures':'Description,Faces,Objects', 'language':'en'}

image_path = "/home/vase/Documents/python/image-analyzer/friends.jpg"
image_data = open(image_path, "rb").read()

headers    = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}

response = requests.post(address, headers=headers, params=parameters, data=image_data)

response.raise_for_status()

result = response.json()
app = Draw(result)

img = cv2.imread('friends.jpg')
scanFaces = input("Choose to scan faces or objects {f/o}")
additionalInfo = input("Do you like more functionality? {y/n}")

if scanFaces == "f":
    app.drawFace()
elif scanFaces == "o":
    app.drawObject()
else:
    quit()

if additionalInfo == "y":
    app.additionalInfo()

app.displyImg()
