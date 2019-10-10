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

import cv2 as cv2
import numpy as np


def accumulateHomographies(Hpair, m):
    # Result
    Htot = []
    i = 0

    if len(Hpair) == 2:  # only two frames
        H1 = np.matmul(Hpair[1], Hpair[0])
        H2 = np.identity(3)
        H3 = np.matmul(np.linalg.inv(Hpair[0]), np.linalg.inv(Hpair[1]))
        Htot.append(H1)
        Htot.append(H2)
        Htot.append(H3)
        return Htot

    while i <= len(Hpair):

        # more than 2 frames - 3 cases:
        # CASE 1 --> i < m
        if i < m:
            H_im = Hpair[m]
            k = m - 1
            while k >= i:
                H_im = np.matmul(H_im, Hpair[k])
                k -= 1
            Htot.append(H_im)
            i += 1

        # print("AFTER CASE 1 current index: "+ str(i))
        # CASE 2 --> i == m
        elif i == m:
            H_im = np.identity(3)
            Htot.append(H_im)
            i += 1


        # CASE 3 --> i > m
        else:
            k = m + 1
            H_im = np.linalg.inv(Hpair[m])
            while k < i:
                inverseH = np.linalg.inv(Hpair[k])
                H_im = np.matmul(H_im, inverseH)
                k += 1
            Htot.append(H_im)
            i += 1
    return Htot


def renderPanorama(folderPath, my_images_GBR, Htot):
    panoImg = [];
    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    for i in range(len(my_images_GBR)):
        img = my_images_GBR[i]
        warped = cv2.warpPerspective(img, Htot[i], (img.shape[1], img.shape[0]))
        if i == 0:
            panoImg = img
        panoImg = cv2.addWeighted(panoImg, 1, warped , 0.3, 0)
    return trim(panoImg)

def trim(frame):
    # trims the black residue in the panorama image
    #crop top
    if not np.sum(frame[0]):
        return trim(frame[1:])
    #crop bottom
    elif not np.sum(frame[-1]):
        return trim(frame[:-2])
    #crop left
    elif not np.sum(frame[:,0]):
        return trim(frame[:,1:])
        #crop right
    elif not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])
    return frame


def StitchPanorama(my_images_GBR):  #NOT GOOD DOES NOT DO WRAPPING
    # stitch the images together to create a panorama
    stitcher = cv2.createStitcher(False)
    (status, stitched) = stitcher.stitch(my_images_GBR, showMatches=True)
    # (result, vis) = stitcher.stitch(my_images_GBR, showMatches=True)  # result is panorama
    return stitched


def outputPanorama(panoImg, fileName):
    cv2.imwrite('../data/out/example/' + fileName + '.png', panoImg)
