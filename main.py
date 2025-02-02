from cv2 import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import re
import string
import json
import pandas as pd

#setting up path to the exe file

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe" #please change this location with the locatio of your exe file

#loading the image
img = cv2.imread('1.jpeg',0)# chnage this with your image and add path if it is not in same directory
img1 = cv2.imread('2.jpeg',0)
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # Detect faces

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = face_cascade.detectMultiScale(gray, 1.2, 2)

# # Draw rectangle around the faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

########################################custom fuctions#####################################################

#convert to grayscale
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction(special use case -)
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

###################################### ends#############################################################

# image_gray = get_grayscale(img)
# image_canny = canny(img)
# image_deskew = deskew(img)
# image_opening = opening(img)


#applying my custom functions
img = remove_noise(img)
image_erode = erode(img)
img_final = cv2.GaussianBlur(image_erode,(5,5),0)

img1 = remove_noise(img1)
image_erode1 = erode(img1)
img_final1 = cv2.GaussianBlur(image_erode1,(5,5),0)

cv2.namedWindow('Filtered Image First',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Filtered Image First', 400,450)
cv2.imshow("Filtered Image First",img_final)

cv2.namedWindow('Filtered Image Second',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Filtered Image Second', 400,450)
cv2.imshow("Filtered Image Second",img_final1)

# cv2.imshow("my image",image_canny)
# cv2.imshow("my image",image_deskew)
# cv2.imshow("my image",image_opening)
#cv2.imshow("my image",image_erode)


cv2.namedWindow('Original Image First',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original Image First', 400,450)
cv2.imshow("Original Image First",img)

cv2.namedWindow('Original Image Second',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original Image Second', 400,450)
cv2.imshow("Original Image Second",img1)

#showing the images
cv2.waitKey()
cv2.destroyAllWindows()


# Adding custom options
custom_config = r'--oem 3 --psm 6'
test_string = pytesseract.image_to_string(img_final,config=custom_config).lower()
x = test_string.splitlines()
# print(type(x))
# print(x)
# print ("The list of words is : " +  str(res))
# d = pytesseract.image_to_data(img, output_type=Output.DICT)
# keys = list(d.keys())
# print("this is data",d)
# df = pd.DataFrame(x)
# print(df)

#custom code to detech only
print(x)
def check(sentence, words):
    res = [all([k in s for k in words]) for s in sentence]
    return [sentence[i] for i in range(0, len(res)) if res[i]]

# Driver code to detect only name and roll (i can optimise it)
sentence = x
word1 = ['name']
print("the feilds we require are:-")
y=(check(sentence,word1))
print(y)



# date_pattern = 'Name'

# n_boxes = len(d['text'])
# for i in range(n_boxes):
#     if int(d['conf'][i]) > 60:
#     	if re.match(date_pattern, d['text'][i]):
# 	        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
# 	        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#cv2.imshow('img', img)
#cv2.waitKey(0)

