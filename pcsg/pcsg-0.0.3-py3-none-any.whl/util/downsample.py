import subprocess
from PIL import Image

# increase maximum image buffer size
Image.MAX_IMAGE_PIXELS = Image.MAX_IMAGE_PIXELS * 4




def downsampleImage (input, output, factor):
    """
    Downsample an image
    """
    img = Image.open(input)
    w = int (float(img.size[0]) / float (factor))
    h = int (float(img.size[1]) / float (factor))
    img = img.resize((w, h), Image.ANTIALIAS)
    img.save(output) 
    return True
