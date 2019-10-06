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
    matches_mask = np.ravel().tolist()
    draw_params = dict(matchesMask=matches_mask,
                       singlePointColor=None,
                       matchColor=(255, 0, 0),
                       flags=2)
    res = cv.drawMatches(img1, pos1, img2, pos2, inliers, None, **draw_params)
    cv.imshow('matched images', res)