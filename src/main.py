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
import cv2 as cv2
import math
import os

from collections import OrderedDict
from geometricTransformation import *
from panoramaStitching import *


def generatePanorama():
    imagesDict = loadImagesFromFolder('../data/inp/examples')

    for imgKey in imagesDict:  # runs over all images sequences that makes one new panorama
        counter = 1
        my_images = imagesDict[imgKey]

        for k in my_images:  # runs over each consecutive pair of images
            if k is None:
                print('Could not open or find the images!')
                exit(0)

        homography_list = []  # size = len(my_images)-1

        for k in range(len(my_images) - 1):  # each consecutive images
            fileName = imgKey + str(counter)  # indexing output file name
            corrList = findMatchFeatures(my_images[k], my_images[k + 1])
            #  run RANSAC algorithm
            homography, inliersList = ransacHomography(corrList, 0.75)
            homography_list.append(homography)
            displayMatches(my_images[k], my_images[k + 1], inliersList, fileName)
            counter += 1  # to increase image indexing
        # ************************ AFTER RUNNING ALL PAIR IMAGES ************************
        m = math.ceil(len(my_images) / 2)  # Index of middle image rounded up, for common coordinate system
        # Htot = accumulateHomographies(homography_list, m)



def loadImagesFromFolder(folder):
    images = []
    imgName = ""
    imagesDict = OrderedDict()

    for fileName in os.listdir(folder):
        # first image in folder
        if not imgName:
            imgName = fileName[:-5]

        # new images for new panorama
        if fileName[:-5] != imgName:
            imagesDict.setdefault(imgName, []).extend(images)
            imgName = fileName[:-5]  # new name for new panorama
            images = []  # new list of images for the panorama

        # image is for the same panorama
        img = cv2.imread(os.path.join(folder, fileName), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)

    # last image in folder, need to add the last list to dictionary
    imagesDict.setdefault(imgName, []).extend(images)
    return imagesDict


def main():
    generatePanorama()


if __name__ == "__main__":
    main()
