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