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
    #Result
    Htot = []
    if len(Hpair) == 2:
        H1 = np.matmul(Hpair[1], Hpair[0])
        H2 = np.identity(3)
        H3 = np.matmul(np.linalg.inv(Hpair[0]), np.linalg.inv(Hpair[1]))
        Htot.append(H1)
        Htot.append(H2)
        Htot.append(H3)
        return Htot

    # m>2
    Htemp = []
    # i < m
    for j in range(m):
        k = m-1  #  maybe not here
        H_im = Hpair[k]
        i = k-1
        while i >= j:
            H_im = np.matmul(H_im, Hpair[i])
            i = i-1
        #Htemp.append(H_im)
        Htot.append(H_im)

    # for i in reversed(Htemp):   #the order is ok
    #     Htot.append(i)

    # i == m
    H_im = np.identity(3)
    Htot.append(H_im)

    # i > m
    for j in range(m, len(Hpair)-1):
        H_im = np.linalg.inv(Hpair[j])
        for i in range(j, len(Hpair)):
            inverseH = np.linalg.inv(Hpair[i+1])
            H_im = np.matmul(H_im, inverseH)
        Htot.append(H_im)


    return Htot
