'''
    ! displayMatches FUNCTION !

    runs on an image pair in each one of the provided sequences,
    together with its match points pos1 pos2 (obtained from findFeatures & matchFeatures),
    and inlier index set 'inlind' (obtained from ransacHomography).
    inliers -  blue line
    outliers - yellow line
'''

import cv2 as cv
import numpy as np


def displayMatches(pos1, pos2, img1 , img2, inliers):
    #matches_mask = np.ravel().tolist()
    draw_params = dict(matchesMask=None,
                       singlePointColor=None,
                       matchColor=(255, 0, 0),
                       flags=2)
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
    res = cv.drawMatches(img1, pos1, img2, pos2, inliers, img_matches,  flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv.imshow('matched images', res)