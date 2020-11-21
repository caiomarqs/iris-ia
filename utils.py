from PIL import Image
import cv2
import base64
import io
import numpy as np

# Converte a imagem
def string_to_image(base64_string):
    imgdata = base64.b64decode(str(base64_string[base64_string.find(",")+1:]))
    image = io.BytesIO(imgdata)
    return image