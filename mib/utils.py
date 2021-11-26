from io import BytesIO
import base64
from PIL import Image

import os
from werkzeug.utils import secure_filename

# UTILS FOR FORM CHECKS
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


'''
    Utility function to save a new profile picture.
'''
def save_image(user_id, file):
    filename = 'mib/static/images/user_' + str(user_id) + ".png"
    with open(filename, "wb") as outf:
        outf.write(base64.b64decode(bytes(file, 'UTF-8')))
        
    return filename


'''
    Utility function to check if profile picture has a valid format.
'''
def allowed_file(format):
    return format in ALLOWED_EXTENSIONS


'''
    Utility function for converting a PIL image
    to base64
'''
def image_to_base64(profile_pic: str):
    pic = Image.open(profile_pic)
    buffered = BytesIO()
    pic.save(buffered, format="PNG")
    binary = str(base64.b64encode(buffered.getvalue()))
    binary = binary.replace("b'", "")
    binary = binary.replace("'", "")

    return binary
