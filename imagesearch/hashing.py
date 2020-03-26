import numpy as np
import cv2
import os

def dhash(image,hashSize = 8):
    # convert the img to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # resize the img,add a single column so we can 
    # compute the horizontal gradient

    resized = cv2.resize(gray,(hashSize + 1,hashSize))

    # compute the relative horizental gradient between adjacent
    # column pixels
    diff = resized[:,1:] > resized[:,:-1]

    # convert the difference image to dhash

    return sum([2 ** i for (i,v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    # convert the hash value to int
    return int(np.array(h,dtype = 'float64'))

def hamming(a,b):
    # compute and return the Hamming distance between the integers
    return bin(int(a) ^ int(b)).count('1')

if __name__ == '__main__':
    cwd = os.getcwd()
    print
    image = cv2.imread('H:\searchengine\标书图片\file_blue.png')
    # image = cv2.imread(os.path.join(cwd,'file_blue.png'))
    print(image.shape)
    test_hash = dhash(image)
    print(test_hash)
    



