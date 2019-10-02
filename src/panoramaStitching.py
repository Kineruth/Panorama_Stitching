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