# About
Sometimes i need some background imaged QR code, not boring as the usual black-dotted whited-grounded ones. 
Around the web i founded only websites with bloatware and ADs of any kind and the result is usually not satisfactory.
So I decided to create this very simple script, i hope that is useful to someone like me.
It wraps the qrcode lib to generate QR codes.


# Setup
Clone the project and enter inside a directory project.

Then create a venv envirnoment as usual in python.

```python3 -m venv venv```


Activate the created venv

```source venv/bin/activate```


Install the requirement libraries

```pip install -r requirements.txt```


Run the script to generate a test QR code

```python qrcode-vanity-generator.py -d "hello world"```


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



Generate a QR code for bitcoin address in classic black and white style

```python qrcode-vanity-generator.py -o myaddress.png -d bc1qyd054pemgd9qwsuc4ksl03qhhznrq44mfaamhp --backColor 254 --frontColor 3```


