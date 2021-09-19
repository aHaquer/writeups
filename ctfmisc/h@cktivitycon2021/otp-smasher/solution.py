"""
Your fingers too slow to smash, tbh. 
"""

import pytesseract
from time import sleep
from PIL import Image
import requests

for i in range(3):
    # Download
   
    response = requests.get("http://challenge.ctf.games:32067/static/otp.png")

    file = open("otp.png", "wb")
    file.write(response.content)
    file.close()
    
    # Get text
    text = pytesseract.image_to_string(Image.open("otp.png"), lang='eng', config='digits').strip()
    print(text)

    #sleep(1)
    mykey = {'otp_entry' : text}
    #print(mykey)
    r = requests.post("http://challenge.ctf.games:32067/",data = mykey)
    #print(r.text)


response = requests.get("http://challenge.ctf.games:32067/static/flag.png")
file = open("flag.png", "wb")
file.write(response.content)
file.close()

# Get text
text = pytesseract.image_to_string(Image.open("flag.png"), lang='eng').strip()
print(text)
