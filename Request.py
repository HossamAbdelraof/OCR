import json
import requests
import time
from PIL import Image, ImageDraw

subscription_key = "20d4fbf92f884f349db21874dd04186a"
endpoint = "https://first-vision.cognitiveservices.azure.com/"

text_recognition_url = endpoint + "/vision/v3.1/read/analyze"


image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

image= 'C:\\Users\\20812018100700\\Downloads\\readsample.jpg'
#headers = {'Ocp-Apim-Subscription-Key': subscription_key}
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}

with open(image, 'rb') as f:
    data = f.read()


#data = {'url': image_url}

response = requests.post(text_recognition_url, headers=headers, data=data)
response.raise_for_status()


operation_url = response.headers["Operation-Location"]




while True:
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()
    # final = json.dumps(analysis, indent=4)
    # print(final)

    time.sleep(1)
    if ("analyzeResult" in analysis):
        break
    if ("status" in analysis and analysis['status'] == 'failed'):
        break


final_text = [(line["boundingBox"], line["text"])
               for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

print(final_text)






"""
draw in image

img =  Image.open(image).convert('RGBA')
txt = Image.new('RGBA', img.size, (255,255,255,0))
d = ImageDraw.Draw(txt)
d.rectangle(
   (38, 650, 2572, 815),
   fill=(255, 0, 0),
   outline=(0, 0, 0))
d.rectangle(
   (184, 1053, 580, 1128),
   fill=(255, 255, 0),
   outline=(0, 0, 0))


out = Image.alpha_composite(img, txt)


out.show()

"""

