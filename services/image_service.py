import base64
from io import BytesIO
from PIL import Image
import numpy as np

class ImageService:
    def load_image_from_base64(self, encoded_image):
        sanitized_encoded_data = encoded_image.split(',')[1]
        decoded_data = base64.b64decode(sanitized_encoded_data)
        pil_image = Image.open(BytesIO(decoded_data))
        return np.array(pil_image)
