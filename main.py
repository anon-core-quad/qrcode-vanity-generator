import qrcode
import segno

from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import ImageColorMask
import numpy as np


# 1. Generate QR code with high error correction
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=1
)
qr.make(fit=True)


qr.add_data('https://example.com')
# img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
#img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))

# 2. Load and resize logo
logo = Image.open("/home/loth/Pictures/tuscany_hills.png")
#logo = logo.resize((qr.pixel_size, qr.pixel_size), Image.LANCZOS)

# 4. Save result
#img.save("qr_code_with_logo.png")   

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=GappedSquareModuleDrawer(),
    eye_drawer=RoundedModuleDrawer(),
    #color_mask=ImageColorMask(color_mask_path='/home/loth/Pictures/tuscany_hills.png'),
    fill_color=(0, 0, 0),  # dark modules stay opaque
    back_color=(255, 255, 255),
)
img.save("aaaaa.png")   




#img = img.convert('RGB')

# Load and resize background image to match QR size
img = Image.open('aaaaa.png').convert('RGBA').resize(img.size)


# Make white pixels transparent using numpy (fast)
arr = np.array(img)
arr[arr[:, :, :3] == [255, 255, 255], 3] = 0  # set alpha=0 where white
img = Image.fromarray(arr)

# Load new background
bg = Image.open('/home/loth/Pictures/hyperspace.jpeg').convert('RGBA').resize(img.size)

# Composite: transparent areas show background
result = Image.alpha_composite(bg, img)
result.convert('RGB').save('result.png')










# Composite: where QR is white (255) → show bg, where dark (0) → keep black
#mask = img.convert('L')
#result = Image.composite(img, bg, mask)
#result.save('qr_gapped_bg.png')
#
#
#img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
#img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
#img_3 = qr.make_image(image_factory=StyledPilImage, embedded_image_path="/home/loth/Pictures/tuscany_hills.png")
#
#img_1.save("test1.png")   
#img_2.save("test2.png")   
#img_3.save("test3.png")   



#qr = segno.make('https://example.com', error='h')
#qr.to_artistic(
#    background='/home/loth/Pictures/hyperspace.jpeg',
#    target='aaaaa2.png',
#    scale=8
#)   