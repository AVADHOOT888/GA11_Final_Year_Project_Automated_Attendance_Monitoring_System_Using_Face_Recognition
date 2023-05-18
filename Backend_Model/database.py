import os
from os import listdir
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
import numpy as np
import pickle
import cv2
import base64
from keras_facenet import FaceNet  
import openpyxl
from pytz import timezone 
import pandas as pd
import datetime
from IPython.display import display, Javascript
# from google.colab.output import eval_js
from base64 import b64decode
from IPython.display import Image
MyFaceNet=FaceNet()
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))


database = {}
folder='Students/Images/'
students=[]


for filename in listdir(folder):
    path = folder + filename
    gbr1 = cv2.imread(path)
    if(gbr1 is not None):
      students.append(filename.split(".")[0])
    
    if gbr1 is None:
        print(f"Error reading image {filename}")
        continue
    
    wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
    if len(wajah) == 0:
        print(f"No face detected in image {filename}")
        continue
    
    x1, y1, width, height = wajah[0]
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    
    gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
    gbr = Img.fromarray(gbr)
    gbr_array = np.array(gbr)
    
    face = gbr_array[y1:y2, x1:x2]
    face = Img.fromarray(face)
    face = face.resize((160, 160))
    face = np.array(face)
    
    face = np.expand_dims(face, axis=0)
    signature = MyFaceNet.embeddings(face)
    
    database[os.path.splitext(filename)[0]] = signature
myfile = open("data.pkl", "wb")
pickle.dump(database, myfile)
myfile.close()

myfile = open("data.pkl", "rb")
database = pickle.load(myfile)
myfile.close()

# print(database)


import pickle
myfile = open("data.pkl", "wb")
pickle.dump(database, myfile)
myfile.close()

myfile = open("data.pkl", "rb")
database = pickle.load(myfile)
myfile.close()

# print(database)
print(students)