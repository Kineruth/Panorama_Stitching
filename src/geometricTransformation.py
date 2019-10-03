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

def findMatchFeatures(img1, img2):
    # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    detector = cv.xfeatures2d.SIFT_create(0, 3, 0)
    # detector = cv.xfeatures2d_SURF.create(hessianThreshold=minHessian)
    
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

    # -- Step 2: Matching descriptor vectors with a FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)

    # -- Filter matches using the Lowe's ratio test
    ratio_thresh = 0.5
    good_matches = []
    good_matches2 = []
    corrList = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)
            good_matches2.append(n)
            img1_idx = m.queryIdx
            img2_idx = n.trainIdx
            [x1, y1] = keypoints1[img1_idx].pt
            [x2, y2] = keypoints2[img2_idx].pt
            corrList.append([x1,y1, x2, y2])
            #  pos2.append([x2, y2])
    #  print(corrList)
    return corrList



