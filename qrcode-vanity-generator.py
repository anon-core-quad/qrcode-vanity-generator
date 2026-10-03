#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
qrcode-vanity-generator.py

Description:
    Brief summary of what this script does.

Author: anon_core_quad_9999
Email: anon_core_quad@proton.me
Date: 2026-10-03
Version: 1.0
License: GPL 3
"""

import sys
import qrcode
import numpy as np
import argparse

from PIL import Image
from PIL import ImageEnhance
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, GappedSquareModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, ImageColorMask


parser = argparse.ArgumentParser(description="QR Code vanity generator")
parser.add_argument("-o", "--output", default="result.png", help="Output QR code file")
parser.add_argument("-bc", "--backColor", type=int, default=254, help="Output QR code file")
parser.add_argument("-c", "--frontColor", type=int, default=3, help="Output QR code file")
parser.add_argument("-fg", "--foreground", help="Specify image used inside the QR points")
parser.add_argument("-cfg", "--centeredForeground", action='store_true', help="Specify image used at center of the QR points")
parser.add_argument("-bg", "--background", help="Specify image used in the background, instead of white")
parser.add_argument("-b", "--brightness", type=int, default=0.8, help="Default 0.8. Use it for estetic reason or if the QR code doesn't work. Tipically the modules of QR code must have a difference of about 40 percent of brightness with the background")
parser.add_argument("-d", "--data", required=True, help="String encoded inside the QR code generated")
args = parser.parse_args()


if args.centeredForeground and not args.foreground:
    parser.error('--foreground is required when --centeredForeground is given')

resultImage = args.output
foregroundImage = args.foreground
backgroundImage = args.background
dataQRCode = args.data
backColor = args.backColor
frontColor = args.frontColor
bgBrightnessAdjustment = args.brightness
centeredLogo = args.centeredForeground

outputPath = "./outputs/"

# Generate QR code with high error correction
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=40,
    border=1
)
qr.make(fit=True)
qr.add_data(dataQRCode)

# The variable where i'll save the rendered qrcode
img = None

if foregroundImage is None:
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=GappedSquareModuleDrawer(),
        eye_drawer=SquareModuleDrawer(),
        # color_mask=RadialGradiantColorMask(
        #     back_color=(255, 255, 255),
        #     center_color=(250, 250, 250),
        #     edge_color=(0, 0, 0),
        # ),
        color_mask=SolidFillColorMask(
            front_color=(frontColor, frontColor, frontColor),
            back_color=(backColor, backColor, backColor),
        )
    )
else:
    if centeredLogo:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            eye_drawer=SquareModuleDrawer(),
            color_mask=SolidFillColorMask(
                front_color=(frontColor, frontColor, frontColor),
                back_color=(backColor, backColor, backColor),
            ),
            embedded_image_path=foregroundImage
        )
    else:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            eye_drawer=SquareModuleDrawer(),
            color_mask=ImageColorMask(color_mask_path=foregroundImage)
        )

img = img.convert('RGBA')

# Array of (H, W, 4)
arr = np.array(img)

qrHeight=arr.shape[0]
qrWidth=arr.shape[1]
finalDestination = outputPath + resultImage


if backgroundImage is None:
    img.save(finalDestination)

else:
    # Make white pixels transparent using numpy (fast)
    mask = np.all(arr[:, :, :3] == backColor, axis=2)
    arr[mask, 3] = 0

    img = Image.fromarray(arr)

    # Load new background
    bg = Image.open(backgroundImage).convert('RGBA').resize(img.size)
    bg = ImageEnhance.Brightness(bg).enhance(bgBrightnessAdjustment)

    # Composite: transparent areas show background
    result = Image.alpha_composite(bg, img)

    result.convert('RGB').save(finalDestination)

