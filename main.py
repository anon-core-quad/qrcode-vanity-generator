import qrcode
import segno
import numpy as np
import argparse

from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import ImageColorMask


parser = argparse.ArgumentParser(description="My script")
parser.add_argument("-o", "--output", default="out.txt", help="Output file")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
parser.add_argument("--count", type=int, default=1, help="Number of iterations")

args = parser.parse_args()
print(args.output, args.verbose, args.count)

outputPath = "./outputs/"
importedImages = "./images/"
dataQRCode = 'https://example.com'

backgroundImage = 'hyperspace.jpeg'
foregroundImage = "tuscany_hills.png"
resultImage = 'result.png'

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
    module_drawer=GappedSquareModuleDrawer(),
    eye_drawer=RoundedModuleDrawer(),
    #color_mask=ImageColorMask(color_mask_path=importedImages + foregroundImage),
    color_mask=RadialGradiantColorMask(),
    fill_color=(0, 0, 0),  # dark modules stay opaque
    back_color=(255, 255, 255),
)

#img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
#img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
#img_3 = qr.make_image(image_factory=StyledPilImage, embedded_image_path="/home/loth/Pictures/tuscany_hills.png")

img = img.convert('RGBA')



#print(img.mode)   # should print "RGBA"
arr = np.array(img)
#print(arr.shape)  # should print (H, W, 4)

#print(arr)


qrHeight=arr.shape[0]
qrWidth=arr.shape[1]

#img.save(outputPath + "aaaaa.png")   

# Load and resize background image to match QR size
#img = Image.open(outputPath + 'aaaaa.png').convert('RGBA').resize(img.size)


# Make white pixels transparent using numpy (fast)
#arr[arr[:, :, :3] == [255, 255, 255], 3] = 0  # set alpha=0 where white

for y in range(qrHeight):
    for x in range(qrWidth):
        if arr[y, x, 0] == 255 and arr[y, x, 1] == 255 and arr[y, x, 2] == 255:
            arr[y, x, 3] = 0


img = Image.fromarray(arr)


# Load new background
bg = Image.open(importedImages + backgroundImage).convert('RGBA').resize(img.size)

# Composite: transparent areas show background
result = Image.alpha_composite(bg, img)
result.convert('RGB').save(outputPath + resultImage)










# Composite: where QR is white (255) → show bg, where dark (0) → keep black
#mask = img.convert('L')
#result = Image.composite(img, bg, mask)
#result.save(outputPath + 'qr_gapped_bg.png')
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
#    target=outputPath + 'aaaaa2.png',
#    scale=8
#)   