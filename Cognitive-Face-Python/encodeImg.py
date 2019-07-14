# Import the base64 encoding library.
import base64
import sys

# Pass the image data to an encoding function.
def encode_image(image):
  #image_content = image.read()
  return base64.b64encode(image.read())
encode_image(sys.argv[1])
