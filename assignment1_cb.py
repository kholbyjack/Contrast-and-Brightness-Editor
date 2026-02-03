import cv2 as cv
import numpy as np
import keyboard as kb
import os

# default values
alpha = 1.0
beta = 0

# loading image
# ---altered files are called out.bmp
if os.path.isfile('out.bmp'):
    image = cv.imread('out.bmp')
    os.remove('out.bmp')
else:
    image = cv.imread('dog.bmp')

if image is None:
    print('Image does not exist.')
    exit(0)

# new preview image 
new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)


# trackbar action implementation
# ---contrast is changed by updating alpha
# ---values from 0 to 100 scaled to be between 0 and 2
def contrast_action(value):
    if value == 0:
        alpha = 0
    else:
        alpha = value / 50
    global save_image
    save_image = cv.convertScaleAbs(new_image, alpha=alpha)
    cv.imshow('New Image', save_image)
    
    new_hist_display = np.zeros((256, 256, 3),  dtype=np.uint8)
    new_hist_display[:] = [255, 255, 255]
    hist(save_image, new_hist_display)      # update histogram
    cv.imshow('New Histogram', new_hist_display)


# ---brightness is updated by changing beta value to be between 0 and 255
def brightness_action(value):
    beta = value
    global save_image
    save_image = cv.convertScaleAbs(new_image, beta=beta)
    cv.imshow('New Image', save_image)
    
    new_hist_display = np.zeros((256, 256, 3),  dtype=np.uint8)
    new_hist_display[:] = [255, 255, 255]
    hist(save_image, new_hist_display)      # update histogram
    cv.imshow('New Histogram', new_hist_display)
    

# saves image
# ---ctrl+enter saves the image
def save():
    cv.imwrite(filename='out.bmp', img=save_image)


# splits channels and calculates histograms for all of them
def hist(image, hist_image):
    channels = cv.split(image)
    colors = {'B', 'G', 'R'}
    for channel, color  in zip(channels, colors):
        hist = cv.calcHist([channel], [0], None, [256], [0, 256])
        draw_hist(hist, hist_image, color)


# draws a color image histogram
# ---done with line fucntion, for all RGB channels
def draw_hist(hist, image, color):
    cv.normalize(hist, hist, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    for index, value in enumerate(hist):
        if color == 'R':
            cv.line(image, (index, 256), (index, 256 - int(value)), (0, 0, 255), 1)
        elif color == 'G':
            cv.line(image, (index, 256), (index, 256 - int(value)), (0, 255, 0), 1)
        elif color == 'B':
            cv.line(image, (index, 256), (index, 256 - int(value)), (255, 0, 0), 1)


#empty np images for drawing histgram on
hist_display = np.zeros((256, 256, 3), dtype=np.uint8)      
new_hist_display =  np.zeros((256, 256, 3), dtype=np.uint8)
hist_display[:] = [255, 255, 255]
new_hist_display[:] = [255, 255, 255]

#call function for displayng the histograms for both images
hist(image, hist_display)       
hist(new_image, new_hist_display)

# display four windows for images and histograms
cv.namedWindow('Original Image', cv.WINDOW_AUTOSIZE)
cv.imshow('Original Image', image)

cv.namedWindow('New Image', cv.WINDOW_AUTOSIZE)
cv.imshow('New Image', new_image)

cv.namedWindow('Histogram', cv.WINDOW_AUTOSIZE)
cv.imshow('Histogram', hist_display)

cv.namedWindow('New Histogram', cv.WINDOW_AUTOSIZE)
cv.imshow('New Histogram', new_hist_display)

# trackbars
# ---contrast will be from 0 to 2, with 50 being 1
cv.createTrackbar('Contrast', 'New Image', 0, 100, contrast_action)
cv.createTrackbar('Brightness', 'New Image', 0, 255, brightness_action)

# keyboard shortcut for saving
kb.add_hotkey('ctrl+enter', save)

# program ends when windows are closed
while True:
    key = cv.waitKey(0)
    if key == ord('l'):
        cv.destroyAllWindows()
        break