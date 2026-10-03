# About
Sometimes i need some background imaged QR code, not boring as the usual black-dotted whited-grounded ones. 
Around the web i founded only websites with bloatware and ADs of any kind and the result is usually not satisfactory.
So I decided to create this very simple script, i hope that is useful to someone like me.
It wraps the qrcode lib to generate QR codes.


# Setup
Just install the library requirements.

``` pip install -r requirements.txt ```


# Usage


Generate a white dotted qrcode with image background specified 

```python qrcode-vanity-generator.py -d example.com --background image_examples/child_birthday.jpeg```



Generate a white dotted qrcode with image background specified 

```python qrcode-vanity-generator.py -o hyperspace-qr.png -d example.com --foreground image_examples/hyperspace.jpeg```



Generate a QR code with a centered logo, specify the output filename

```python qrcode-vanity-generator.py -o novarcsrl-com.png -d novarcsrl.com --centeredForeground --foreground image_examples/logo.jpeg```



Generate a QR code with a brightness adjustment to read the dots more easly

```python qrcode-vanity-generator.py -o qr-hills.png -b 1 -d site.com --background image_examples/tuscany_hills.png```



Generate a QR code with gray background and white dots

```python qrcode-vanity-generator.py -o gray.png -d site.com --backColor 44 --frontColor 200```