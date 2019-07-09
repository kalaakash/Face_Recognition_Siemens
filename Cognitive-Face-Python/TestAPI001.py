'''import SDKClient 
import FaceClient

creds = '0af57de2a87249e19e11c118b0ba3ab8'

endpoint = ""

SDKClient(creds, config)

FaceClient(endpoint, credentials)

'''
import cognitive_face as CF

# Replace with a valid subscription key (keeping the quotes in place).
KEY = '0af57de2a87249e19e11c118b0ba3ab8'
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

landmarks = faces[0].FaceLandmarks

#print(faces)
print(faces[0])
print(faces[1])
print(landmarks)