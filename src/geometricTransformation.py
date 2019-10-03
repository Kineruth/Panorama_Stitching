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
import random

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

def applyHomography(randomFour):
    # loop through correspondences and create assemble matrix
    aList = []
    for r in randomFour:
        p1 = np.ndarray([r.item(0), r.item(1), 1]) #2 pairs of matched points
        p2 = np.ndarray([r.item(2), r.item(3), 1]) #2 pairs of matched points
#********************************
        a2 = [0, 0, 0, -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
              p2.item(1) * p1.item(0), p2.item(1) * p1.item(1), p2.item(1) * p1.item(2)]
        a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2), 0, 0, 0,
              p2.item(0) * p1.item(0), p2.item(0) * p1.item(1), p2.item(0) * p1.item(2)]
        aList.append(a1)
        aList.append(a2)

    matrixA = np.ndarray(aList)

    # svd composition
    u, s, v = np.linalg.svd(matrixA)

    # reshape the min singular value into a 3 by 3 matrix
    h = np.reshape(v[8], (3, 3))

    # normalize and now we have h
    h = (1 / h.item(8)) * h
    return h


def geometricDistance(correspondence, h):
        p1 = np.transpose(np.matrix([correspondence[0].item(0), correspondence[0].item(1), 1]))
        estimatep2 = np.dot(h, p1)
        estimatep2 = (1 / estimatep2.item(2)) * estimatep2

        p2 = np.transpose(np.matrix([correspondence[0].item(2), correspondence[0].item(3), 1]))
        error = p2 - estimatep2
        return np.linalg.norm(error)


def ransacHomography(corr, threshold):
        maxInliers = []
        finalH = None
        for i in range(1000):
            # find 4 random points to calculate a homography
            corr1 = corr[random.randrange(0, len(corr))]
            corr2 = corr[random.randrange(0, len(corr))]
            randomFour = np.vstack((corr1, corr2))
            corr3 = corr[random.randrange(0, len(corr))]
            randomFour = np.vstack((randomFour, corr3))
            corr4 = corr[random.randrange(0, len(corr))]
            randomFour = np.vstack((randomFour, corr4))

            # call the homography function on those points
            h = applyHomography(randomFour)
            inliers = []

            for i in range(len(corr)):
                d = geometricDistance(corr[i], h)
                if d < 5:
                    inliers.append(corr[i])

            if len(inliers) > len(maxInliers):
                maxInliers = inliers
                finalH = h
            print
            "Corr size: ", len(corr), " NumInliers: ", len(inliers), "Max inliers: ", len(maxInliers)

            if len(maxInliers) > (len(corr) * threshold):
                break
                return finalH, maxInliers
