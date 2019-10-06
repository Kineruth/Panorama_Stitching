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

from main import pos1, pos2, matches


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
            corrList.append([x1, y1, x2, y2])
            pos1.append([x1, y1])  # save for display lines
            pos2.append([x2, y2])  # save for display lines
    #  print(corrList)
    matches = good_matches
    return corrList


def applyHomography(corrList,h):
    #  transforms pos1 points (from image 1) to pos2 using the homography we found
    #  returns all estimated transposed points (from image 1 to image 2 using homography)
    estimatedPos2 = []
    for i in range(len(corrList)):
        # corr[i] -> [x1,y1,x'1,y'1]
        p1 = np.transpose([corrList[i][0], corrList[i][1], 1])  # p1 = transpose(x1,y1,1) -> homogenic point
        estimateP1 = np.dot(h, p1)  # [x2~,y2~,z2~] = h * p1
        estimateP2 = (1 / estimateP1[2]) * estimateP1  # dividing by the third element
        estimatedPos2.append([estimateP2[0], estimateP2[1]])  # adding estimated point (x1,y1)

    return estimatedPos2


def geometricDistance(corrList, h, inlierTol):
    #  computes
    inliers = []
    estimatedPos2 = applyHomography(corrList, h)
    # print(estimatedPos2)

    for i in range(len(corrList)):
        p2 = np.transpose([corrList[i][2], corrList[i][3], 1])
        estimateP2 = np.transpose([estimatedPos2[i][0], estimatedPos2[i][1], 1])

        error = p2 - estimateP2
        error = np.linalg.norm(error)
        # print(error)

        if error < inlierTol:
            inliers.append(corrList[i])
    return inliers


def calculateHomography(randomFour):
    # loop through correspondences and create assemble matrix
    aList = []
    for r in randomFour:
        p1 = [r[0], r[1], 1]  # 2 pairs of matched points
        p2 = [r[2], r[3], 1]  # 2 pairs of matched points ---> so we have 8 points
        # *************did not understand this:*******************
        a2 = [0, 0, 0, -p2[2] * p1[0], -p2[2] * p1[1], -p2[2] * p1[2],
              p2[1] * p1[0], p2[1] * p1[1], p2[1] * p1[2]]
        a1 = [-p2[2] * p1[0], -p2[2] * p1[1], -p2[2] * p1[2], 0, 0, 0,
              p2[0] * p1[0], p2[0] * p1[1], p2[0] * p1[2]]
        aList.append(a1)
        aList.append(a2)

    #  matrixA = np.ndarray(aList)

    # svd composition (uses least square)
    u, s, v = np.linalg.svd(aList)

    # reshape the min singular value into a 3x3 matrix
    h = np.reshape(v[8], (3, 3))

    # normalize h
    h = (1 / h.item(8)) * h
    return h


def ransacHomography(corrList, threshold):
    maxInliers = []
    finalHomography = None

    for i in range(1000):
        # find 4 random points to calculate a homography
        corr1 = corrList[random.randrange(0, len(corrList))]
        corr2 = corrList[random.randrange(0, len(corrList))]
        randomFour = np.vstack((corr1, corr2))
        corr3 = corrList[random.randrange(0, len(corrList))]
        randomFour = np.vstack((randomFour, corr3))
        corr4 = corrList[random.randrange(0, len(corrList))]
        randomFour = np.vstack((randomFour, corr4))

        # finds the homography function for those points
        h = calculateHomography(randomFour)

        # NEED TO SEND P1 POINTS & H TO applyHomography, then calc Ej & inliers
        # runs over each pair of matched points [x1,y1,x'1,y'1]

        inliers = geometricDistance(corrList, h, 5)  # why inlierTol is 5 ??

        if len(inliers) > len(maxInliers):
            maxInliers = inliers
            finalHomography = h
        # print("CorrList size: ", len(corrList), ", NumInliers: ", len(inliers), ", MaxInliers: ", len(maxInliers))

        if len(maxInliers) > (len(corrList) * threshold):
            break
    return finalHomography, maxInliers
