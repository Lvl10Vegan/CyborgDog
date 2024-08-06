import pandas as pd
import numpy as nm
from PIL import Image, ImageGrab
import pytesseract
import cv2
import time
import sys
import pickle
from socket import *

# Acquire IP for this device, only in use if one wishes to test local transfer
# IP = gethostbyname(gethostname())
# IP = '100.64.218.219' # my current UCSD-Protected IP, change as needed
# TODO: use your own publicly accessed IP for variable IP
# IP = "192.168.1.121" # for aayush's home
IP = "169.228.170.16"
port = 5050 # If port already in use, try changing it
s1 = socket(AF_INET, SOCK_STREAM)
s1.connect((IP, port))

initial = time.time()
data = 0

def createPixelDict():
    # voltage displays are 178 x pixels apart and 87 y pixels apart
    # first xy pair starts at (270,110)
    # screenshots should be 90x50
    xy_arr = []
    init_x = 270
    init_y = 110
    for y in range(3,5):
        for x in range(3):
            xy_arr.append((init_x+178*x, init_y+87*y))

    pixel_dict = {}
    for tup in xy_arr:
        count = xy_arr.index(tup) + 1
        pixel_dict[count] = (2*tup[0], 2*tup[1], 2*tup[0]+91, 2*tup[1]+51)

    return pixel_dict

def takeImage(pixel_dict):
    image_dict = {}
    for key, val in pixel_dict.items():
        image_dict[key] = ImageGrab.grab(bbox=(val[0],val[1],val[2],val[3]))
    # for key, im in image_dict:
    #     im.show()
    return image_dict

def readImage(image_dict):
    pytesseract.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'
    image_read_output = {}
    for key, im in image_dict.items():
        tesstr = pytesseract.image_to_string(cv2.cvtColor(nm.array(im), cv2.COLOR_BGR2GRAY))
        # print(tesstr)
        image_read_output[key] = tesstr
    image_read_output = extractNum(image_read_output)
    # for key in image_read_output:
    #     # print(image_read_output[key])
    return image_read_output

def extractNum(image_read_output):
    str_dict= {}
    for key, read in image_read_output.items():
        first_few = read[0:4]
        no_dot = first_few.replace(".", "")
        no_space = no_dot.replace(" ", "")
        str_dict[key] = no_space
    return str_dict

def toFloat(image_read_output):
    float_dict = {}
    for key, val in image_read_output.items():
        if (val.isnumeric()):
            float_dict[key] = float(val)/100
        else:
            float_dict[key] = 0
            print("read error")
    return float_dict

def readAxis():
    t = time.perf_counter()
    old_floats = {}
    # calling the methods
    pixel_dict = createPixelDict()
    image_dict = takeImage(pixel_dict)
    image_read_output = readImage(image_dict)
    floats = toFloat(image_read_output)
    old_floats = floats
    while (True):
        image_dict = takeImage(pixel_dict)
        image_read_output = readImage(image_dict)
        floats = toFloat(image_read_output)
        electrode_signals = 0
        for key, val in floats.items():
            diff = val - old_floats[key]
            if (diff > 0.1):
                electrode_signals = electrode_signals + 1
        if (electrode_signals > 2):
            print("signal")
            data = 1
            msg = pickle.dumps(data)
            s1.sendall(msg)
            data = 0
        else:
            data = 0
            print("no signal")
            msg = pickle.dumps(data)
            s1.sendall(msg)
        update_time = time.perf_counter()-t
        print(update_time)
        old_floats = floats
        # for key in floats:
        #     print(floats[key])

readAxis()