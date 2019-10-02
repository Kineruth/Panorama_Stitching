'''
    ! displayMatches FUNCTION !

    runs on an image pair in each one of the provided sequences,
    together with its match points pos1 pos2 (obtained from findFeatures & matchFeatures),
    and inlier index set 'inlind' (obtained from ransacHomography).
    inliers -  blue line
    outliers - yellow line
'''