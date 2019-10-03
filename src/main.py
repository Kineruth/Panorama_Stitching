'''
    ! generatePanorama FUNCTION !
    1) read grayscale frames (by their order).
    2) find & match features, between each pair of consecutive frames - findFeatures & matchFeatures FUNCTIONS (in geometricTransformation.py)
    3) register homography pairs - ransacHomography FUNCTION (in geometricTransformation.py)
    4) display inliers & outliers matches, between each pair of consecutive frames - displayMatches FUNCTION (in display.py)
    5) transform the homograpies - accumulateHomographies FUNCTION (in panoramaStitching.py)
    6) load the RGB frames  (in panoramaStitching.py) ????
    7) render panorama of each color channel - renderPanorama FUNCTION (in panoramaStitching.py)

    else:
    upload 2 panorama sequences having the same name conventions the examples - in /data/inp/mine

'''

from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

from geometricTransformation import findMatchFeatures


def generatePanorama():
    img1 = cv.imread('../data/inp/examples/backyard1.jpg', cv.IMREAD_GRAYSCALE)
    img2 = cv.imread('../data/inp/examples/backyard2.jpg', cv.IMREAD_GRAYSCALE)
    img3 = cv.imread('../data/inp/examples/backyard3.jpg', cv.IMREAD_GRAYSCALE)
    my_images = [img1, img2, img3]

    for k in my_images:
        if k is None:
            print('Could not open or find the images!')
            exit(0)

    for k in range(len(my_images) - 1): #  each consecutive images
        print(k)
        corrList = findMatchFeatures(my_images[k], my_images[k + 1])
        #  run RANSAC algorithm
        homography, inliersList = ransac(corrs, estimation_thresh)


generatePanorama();