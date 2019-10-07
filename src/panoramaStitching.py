'''
    Up until here we got a set of registered homographies between each pair of consecutive images.
    Now we want to stitch them together into one panorama frame.
    we pick the coordinate system of the middle (Im) image in the sequence, m=ceil(M/2), in which we want the panorama to be rendered,
    so that all other images (frames) will properly align with it. HOW?

    1) accumulateHomographies
    2) load the RGB frames
    3) translate each set of homographies that transform image coordinates Ii to image Ii+1, into a set of homographies that transform
        image coordinates Ii to image Im (middle) --> using the accumulateHomographies output.
    4) find 4 corner coordinates - this will define the region in which the panorama image Ipano should be rended.
    5) define which parts of Ipano will be obtained from Ii - devide the panorama to M vertical strips, each covering a portion
        of the full lateral range [Xmin, Xmax]
    6) (back)wrap the images on to the strips of the panorama.
'''

import cv2 as cv
import numpy as np


def accumulateHomographies(Hpair, m):  # m was not reduced to (m-1)
    # Result
    Htot = []
    if len(Hpair) == 2:  # only two frames
        H1 = np.matmul(Hpair[1], Hpair[0])
        H2 = np.identity(3)
        H3 = np.matmul(np.linalg.inv(Hpair[0]), np.linalg.inv(Hpair[1]))
        Htot.append(H1)
        Htot.append(H2)
        Htot.append(H3)
        return Htot

    # more than 2 frames - 3 cases:
    # CASE 1 --> i < m
    for i in range(m):
        H_im = Hpair[m]
        k = m - 1
        while k >= i:
            H_im = np.matmul(H_im, Hpair[k])
            k -= 1
        # Htemp.append(H_im)
        Htot.append(H_im)

    # for i in reversed(Htemp): no need to reverse
    #     Htot.append(i)

    '''
    H_tot = [0] * len(Hpair)
    H_down = Hpair[m]  #  already reduced by 1 after ceil(m/2)-1
    for j in range(m-1,-1,-1):  # third is increment
        H_down = H_down * Hpair[j]
        H_tot[j] = H_down
    # i == m
    H_im = np.identity(3)
    Htot.append(H_im)
    '''
    # CASE 2 --> i == m
    if i == m:
        H_im = np.identity(3)
        Htot.append(H_im)
        i += 1

    # CASE 3 --> i > m
    for i in range(m + 1, len(Hpair) - 1):
        k = m + 1
        H_im = np.linalg.inv(Hpair[m])
        while k <= i:
            inverseH = np.linalg.inv(Hpair[k])
            H_im = np.matmul(H_im, inverseH)
            k += 1
        Htot.append(H_im)

    return Htot

def renderPanorama(im, H):
    res = np.ndarray

    return res
