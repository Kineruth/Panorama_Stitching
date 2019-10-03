'''
    1) findFeatures FUNCTION- finding keyPoints using opencv.
    2) matchFeatures FUNCTION - output: a set of points coordinates in both images, of size nx2
                        (that most likely matched, including outliers).
    3) applyHomography FUNCTION
    4) leastSquareHomography
    5) ransacHomography FUNCTION
'''

from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

def findFeatures(img1, img2):

