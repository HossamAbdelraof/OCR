from tkinter import *

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from tkinter import  filedialog


import requests
import time
from PIL import Image, ImageTk
from io import BytesIO

## Define Root
root = Tk()
root.geometry("800x800")


## init frames
##Image screen frame
frame = Frame(root, bd = 5, bg = "purple",  width=500, height=500)
frame.place(x = 10, y=10)

## radio buttons frame
radio_frame = Frame(root, bd = 5)
radio_frame.pack()
radio_frame.place(x = 360, y=480)

## buttons frame
button_frame = Frame(root,  bd = 5)
button_frame.pack()
button_frame.place(x = 590, y=480)

#result frame
res_frame = Frame(root,  bg = "purple", height = 50, width = 50)
res_frame.pack()
res_frame.place(x = 150, y= 550)


## browsing function (open browse dialog)
def browse_image():
    
    file = filedialog.askopenfilenames()
    image_brows.delete(0, END)
    image_brows.insert(0, file[0])


    


## working functions
## get the image and deisplay it on screen
def check_image():# display image in screen 
# if any problem with image display the logo
    
    if link.get() == "1":
        url = image_link.get() 
        try:
            imag = Image.open(BytesIO(requests.get(url).content)).resize((750,450))
            data = ImageTk.PhotoImage(imag)
            screen.configure(image=data)
            screen.image = data
        except:
            screen.configure(image=logo)
            screen.image = logo
    elif(link.get() =="2"):
        try:
            imag = Image.open(image_brows.get()).resize((750,450))
            data = ImageTk.PhotoImage(imag)
            screen.configure(image=data)
            screen.image = data
        except:
            screen.configure(image=logo)
            screen.image = logo
                       

## check if the image is local or online and send request
def OCR():
    
    if link.get() =="1":
        read_response = computervision_client.read(image_link.get(),  raw=True)
        
    elif link.get() =="2":
        image = open(image_brows.get(), "rb")
        read_response = computervision_client.read_in_stream(image, raw=True)
        
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]
    OCR_IMAGE(operation_id)
    
## get result with the operation ID 
def OCR_IMAGE(operation_id):
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        result_label.insert("end",'Waiting for result...')
        time.sleep(1)
    
    if read_result.status == OperationStatusCodes.succeeded:
        result_label.delete("1.0", "end")
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                result_label.insert("end", line.text+"\n")
                print(line.text)



## init logo
url = "https://th.bing.com/th/id/R.20e54f6d90f549baa3eeac3cf3626e30?rik=S2gcf64%2fhOAvfg&pid=ImgRaw"
imag = Image.open(BytesIO(requests.get(url).content)).resize((750,450))
logo = ImageTk.PhotoImage(imag)

   
## init radio buttons states

link = StringVar() # radio string
# setting up online image button
link_radio = Radiobutton(radio_frame, text = "online image",
                         variable = link, value = 1) 

link_radio.pack(padx=5, pady=5, side=LEFT)#setting up online image parameters

# setting up local image button
brows_radio = Radiobutton(radio_frame, text = "browsed image",
                          variable = link, value = 2)
brows_radio.pack(padx=5, pady=5, side = RIGHT)#setting up local image parameter


## checkimage button(display image in screen)
display_but = Button(button_frame, text = "check image", command = check_image)
display_but.pack(padx = 5, pady = 5,  side = LEFT)

## browsing button (open browsing function)
brows_but = Button(button_frame, text = "brows image", command = browse_image)
brows_but.pack(padx = 5, pady = 5, side = RIGHT)

##result button (enable OCR function)
res_but = Button(button_frame, text = "OCR", command = OCR)
res_but.pack(side = LEFT)


## the screen label
screen = Label(frame, width = 750,height = 450, bg="blue", image = logo)
screen.pack()


## set entry fields
## init message 
link_text = StringVar()
link_text.set("past link")

## set title label
link_label = Label(root, textvariable = link_text )
link_label.place(x =10, y = 510)

## set entry field
image_link = Entry(root, width = 40)
image_link.place(x = 80, y = 510)



## init message 
brows_text = StringVar()
brows_text.set("image path")

## set title label
brows_label = Label(root, textvariable = brows_text )
brows_label.place(x =10, y = 480)

## set entry field
image_brows = Entry(root, width = 40)
image_brows.place(x = 80, y = 480)


## set result text field
result_label = Text(res_frame, height = 10, width = 50)
result_label.pack()

## init client
subscription_key = "20d4fbf92f884f349db21874dd04186a"
endpoint = "https://first-vision.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

root.title("OCR")
root.mainloop()





