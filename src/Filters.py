import numpy as np
import cv2 as cv

def negative(image):
    return cv.bitwise_not(image)

def gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def stylisation(image):
    return cv.stylization(image, sigma_s=150, sigma_r=0.25)

def pencil(image):
    dst_gray, dst_color = cv.pencilSketch(image, sigma_s=50, sigma_r=0.06, shade_factor=0.04) # inbuilt function to generate pencil sketch in both color and grayscale
    return dst_color

def emboss(image):
    kernel = np.array([[0,-1,-1], [1,0,-1], [1,1,0]])
    return cv.filter2D(image, -1, kernel)

def sepia(image):
    image = np.array(image, dtype=np.float64) # converting to float to prevent loss
    image = cv.transform(image, np.matrix([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    image[np.where(image > 255)] = 255 # normalizing values greater than 255 to 255
    return np.array(image, dtype=np.uint8) # converting back to int

def binaryThreshold(image):
    ret, image = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    return image

def erosion(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.erode(image, kernel, iterations=1)

def dilation(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.dilate(image, kernel, iterations=1)

def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv.filter2D(image, -1, kernel)

def purpleGreen(image):
    return cv.cvtColor(image, cv.COLOR_HLS2BGR)

def cartoon(image):
    edges1 = cv.bitwise_not(cv.Canny(image, 100, 200)) # for thin edges and inverting the mask obatined
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5) # applying median blur with kernel size of 5
    dst = cv.edgePreservingFilter(image, flags=2, sigma_s=64, sigma_r=0.25) # you can also use bilateral filter but that is slow
    # flag = 1 for RECURS_FILTER (Recursive Filtering) and 2 for  NORMCONV_FILTER (Normalized Convolution). NORMCONV_FILTER produces sharpening of the edges but is slower.
    # sigma_s controls the size of the neighborhood. Range 1 - 200
    # sigma_r controls the how dissimilar colors within the neighborhood will be averaged. A larger sigma_r results in large regions of constant color. Range 0 - 1
    return cv.bitwise_and(dst, dst, mask=edges1) # adding thin edges to smoothened image

def pinkNegative(image):
    return cv.cvtColor(image, cv.COLOR_BGR2HSV)

def purpleUv(image):
    image = sharpen(image)
    return cv.cvtColor(image, cv.COLOR_BGR2Luv)

def cannyBlur(image):
    image = blur(image)
    return canny(image)

#  Blur effect
def blurAverage(image, value):
    value = int(value)
    if value % 2 == 0:
        value += 1
    return cv.blur(image, (value, value))

def blurGaussian(image, value):
    value = int(value)
    if value % 2 == 0:
        value += 1
    return cv.GaussianBlur(image, (value, value), 0)

def blurMedian(image, value):
    value = int(value)
    if value % 2 == 0:
        value += 1
    return cv.medianBlur(image, value)

# Used in Canny filter
def canny(image):
    return cv.Canny(image, 50, 80)

def blur(image):
    return cv.blur(image, (5, 5))