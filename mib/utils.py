import os
import base64

from io import BytesIO

from PIL import Image

# Utils for form checks
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_EMAILS = {
                '@test.com',
                '@test.it',
                '@example.com',
                '@example.it',
                '@hotmail.com',
                '@hotmail.it',
                '@outlook.com',
                '@outlook.it',
                '@gmail.com',
                '@gmail.it',
                '@yahoo.com',
                '@yahoo.it',
                '@studenti.unipi.it',
                '@di.unipi.it'
            }


def save_image(user_id: int, file: str):
    """Utility function for saving a new profile picture."""

    filename = f'mib/static/images/user_{user_id}.png'
    with open(filename, "wb") as outf:
        # Convert from string to base64 binary and saves the image
        outf.write(base64.b64decode(bytes(file, 'UTF-8')))
        
    return filename


def image_to_base64(picture_path: str):
    """Utility function for converting a PIL image to binary base64."""

    pic = Image.open(picture_path)
    buffered = BytesIO()
    pic.save(buffered, format="PNG")
    binary = str(base64.b64encode(buffered.getvalue()))

    # Clear up the result string
    binary = binary.replace("b'", "")
    binary = binary.replace("'", "")

    return binary


def allowed_file(format):
    """Utility function for checking if the profile picture has valid format."""
    return format in ALLOWED_EXTENSIONS


def allowed_email(email):
    """Utility function for checking if the email has valid format."""

    for e in ALLOWED_EMAILS:
        if str(email).endswith(e):
            return True
            
    return False
