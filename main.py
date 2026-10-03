import qrcode
import numpy as np
import argparse

from PIL import Image
from PIL import ImageEnhance

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, GappedSquareModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, ImageColorMask


parser = argparse.ArgumentParser(description="My script")
parser.add_argument("-o", "--output", default="result.png", help="Output QR code file")
parser.add_argument("-fg", "--foreground", help="Specify image used inside the QR points")
parser.add_argument("-bg", "--background", help="Specify image used in the background, instead of white")
parser.add_argument("-d", "--data", help="Number of iterations")

args = parser.parse_args()

outputPath = "./outputs/"
importedImages = "./images/"

resultImage = args.output
foregroundImage = args.foreground
backgroundImage = args.background
dataQRCode = args.data

# Debug
dataQRCode = 'https://example.com'
foregroundImage = "tuscany_hills.png"
backgroundImage = 'tuscany_hills.png'

bgNeutralColor = 1
bgBrightnessAdjustment = 0.8

# 1. Generate QR code with high error correction
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=40,
    border=1
)
qr.make(fit=True)
qr.add_data(dataQRCode)

img = qr.make_image(
    image_factory=StyledPilImage,
    #module_drawer=GappedSquareModuleDrawer(),
    module_drawer=GappedSquareModuleDrawer(),
    eye_drawer=SquareModuleDrawer(),
    #color_mask=ImageColorMask(color_mask_path=importedImages + foregroundImage),
    # color_mask=RadialGradiantColorMask(
    #     back_color=(255, 255, 255),
    #     center_color=(250, 250, 250),
    #     edge_color=(0, 0, 0),
    # ),
    color_mask=SolidFillColorMask(
        front_color=(254, 254, 254),   # white modules
        back_color=(bgNeutralColor, bgNeutralColor, bgNeutralColor),          # dark background
    ),
    #embedded_image_path="/home/loth/Pictures/tuscany_hills.png"
)

img = img.convert('RGBA')


#print(img.mode)   # should print "RGBA"
arr = np.array(img)
#print(arr.shape)  # should print (H, W, 4)

#print(arr)


qrHeight=arr.shape[0]
qrWidth=arr.shape[1]

#img.save(outputPath + "aaaaa.png")   

# Make white pixels transparent using numpy (fast)
#arr[arr[:, :, :3] == [255, 255, 255], 3] = 0  # set alpha=0 where white

for y in range(qrHeight):
    for x in range(qrWidth):
        if arr[y, x, 0] == bgNeutralColor and arr[y, x, 1] == bgNeutralColor and arr[y, x, 2] == bgNeutralColor:
            arr[y, x, 3] = 0


img = Image.fromarray(arr)

# Load new background
bg = Image.open(importedImages + backgroundImage).convert('RGBA').resize(img.size)
bg = ImageEnhance.Brightness(bg).enhance(bgBrightnessAdjustment)


# Composite: transparent areas show background
result = Image.alpha_composite(bg, img)

result.convert('RGB').save(outputPath + resultImage)


