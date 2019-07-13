'''
import requests
from io import BytesIO
from PIL import Image, ImageDraw
'''
import pandas as pd
import cognitive_face as CF

# Replace with a valid subscription key (keeping the quotes in place).

key_data=pd.read_csv("key_data.txt", delim_whitespace=True, skipinitialspace=True)
KEY = key_data.columns[0]
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img1_url = 'Images\IMG_0835.jpg'
img2_url = 'Images\IMG_0836.jpg'

faces = {}

faces = CF.face.detect(img1_url)
faces.append(CF.face.detect(img2_url)[0])
#print(faces)
print(faces[0])
print(faces[1])


if faces[0].get('faceId') == faces[1].get('faceId'):
    print('Same faces')
else:
    print('Different Faces')

#print(faces[0].get('faceRectangle'))
#print(faces[1].get('faceRectangle'))

'''
# Convert width height to a point in a rectangle

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


# Download the image from the url
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

# For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')

# Display the image in the users default image browser.
img.show()
'''