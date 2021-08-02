from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


subscription_key = "20d4fbf92f884f349db21874dd04186a"
endpoint = "https://first-vision.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(
                            endpoint, 
                            CognitiveServicesCredentials(
                                                subscription_key))
read_image_url = "https://4.bp.blogspot.com/-Kr7ZAxi3eYQ/Us0G17B1rzI/AAAAAAAACMg/mHAUFvUPtjc/s1600/messy+handwriting17.jpg"


read_response = computervision_client.read(read_image_url,  raw=True)
# read_response = computervision_client.read_in_stream("inage dir",  raw=True)

read_operation_location = read_response.headers["Operation-Location"]

operation_id = read_operation_location.split("/")[-1]

read_result = computervision_client.get_read_result(operation_id)

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)
# Print the detected text, line by line
text = read_result.analyze_result.read_results
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)