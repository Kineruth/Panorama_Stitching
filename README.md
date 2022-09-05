**Date: 9/10/2019**  
**Last Edit: 26/10/2019**

Panorama Registration & Stitching
===

**Project source can be downloaded from:**
https://github.com/Kineruth/Panorama_Stitching  
This program is a project for Ariel University's Image Processing course. 

Authors:
--
Kineret Ruth Nahary   
Doriya Spielman  
Levi Dworkin 

**Introduction**
==

About the project:
--
*Image stitching* is the process of combining multiple photographic images with overlapping fields of view to produce a segmented panorama or high-resolution image. The most common approaches to image stitching require exact overlaps between images and identical exposures to produce seamless results.  
The human visual system has a field of view of around 135 x 200 degrees, but a typical camera has a field of view of only 35 x  50 degrees. Therefore, panoramic image mosaicking works by taking lots of pictures from an ordinary camera and stitching them together to form a composite image with a much larger field of view.   
The quality of image stitching is measured by the similarity of the stitched image to each of the input images. It also can be measured by the visibility of the seam between the stitched images.  

**Approach And Method**
==

Resignation:
--
* ***Feature Extraction (SIFT):***  
For each pair of consecutive frames in our image sequence, we use scale-invariant feature transform (SIFT) to detect and describe   local features between them. The SIFT enables reliable image matching with various orientation and zoom. The basic steps of the         extraction algorithm are Scale-space extrema detection, keypoint localization, orientation assignment and keypoint descriptor. 
* ***Feature matching (BF):***  
 After finding all the feature points in both images, we use Brute-Force Matcher to match those feature points to each other.   
The algorithm runs over each keypoint ![equation](http%3A%2F%2Fbit.ly%2F2Pmwi9V) from the first set (image) and takes every keypoint in the second set and calculates the distance. The keypoint ![equation](http%3A%2F%2Fbit.ly%2F2WgjKSN) with the smallest distance will be considered its pair. The algorithm returns a set of all matched keypoints. 
* ***Registering the transformation:***  
When matching the SIFT feature points using BF, there will be lots of mismatches. The RANSAC algorithm can be used to remove the mismatches by finding the transformation matrix of these feature points.    
**RANSAC** (RANdom  SAmple  Consensus)  is a  non-deterministic algorithm because it doesn’t ensure to return acceptable results. It is used to estimate parameters for the Homography of a mathematical model from a set of observed data that contains outliers iteratively.    
RANSAC  loop involves:   
1. selects four random feature pairspoint.  
2. computes their homography H using least square (SVD composition).  
3. computes estimated points of the second frame using the homography that was calculated.   
4. computes inliers - if ![equation](http%3A%2F%2Fbit.ly%2F36b3s1V)  where j=1..N and inlierTol=some constant threshold, then it is added as an inlier.  
5. keeps the largest set of inliers and its homography.  
When finished, RANSAC  will return the maximum set of inliers found between each pair of frames and the transformation matrix of its feature points (H).  
We chose inlierTol=10 because we saw it gives a good amount of inliers sets - quite a bit and not much either. 

Panorama Stitching:
--
* ***Transforming into a common coordinate system:***  
We need to choose a coordinate system in which we would like the panorama to be rendered. We chose it to be the coordinate system of the middle frame ![equation](http%3A%2F%2Fbit.ly%2F345vA4K) in our image sequence and transformed all other frames to that coordinate system.   
The resulting panorama image will have a frame I_m coordinate system and be composed of all the transformed frames back-warped so that they properly align with it.  

* ***Rendering the panorama:***  
So far, we have H_tot  that is a set of M homographies 〖H~〗_(i,m )where i=1..M and M is the amount of frames, that transforms pixel coordinates in frame I_(i )to the panorama coordinate system.   
First, we need to define where we want the panorama image I_pano to be rendered. We would like this region to be large enough to include all pixels from all frames. For that, we define which parts of I_pano should be obtained from each frame I_i.   
We divide the panorama to M vertical strips and finally, we Back-Warp the images on the strips of the panorama using H_tot.  
We did not succeed implementing the way was instructed, so we used opencv function wrapPerspective.  

Results
==

The experiments we have done:
--
* ***findFeatures -*** we debated between SURF and SIFT algorithms and decided to go with SIFT because people say it is more used for implementing finding features in image stitching.   
* ***matchFeatures -*** at first we matched descriptor vectors with a Flann based Matcher, but saw that it does not return accurate matched values, so we switched to Brute-Force Matcher and it gave much more accurate results.   
* ***Choosing threshold (inlierTol) -*** we ran our implementation on our input pictures:  
1. for threshold = 5 →  got around 115 inliers.   
2. for threshold = 10 →  got around 110~120 inliers.  
3. for threshold = 20 →  got around 120~130 inliers.  
So we used  threshold=10 because it looked the most accurate for the eye.  

Our final results:
--
1.	***DisplayMatches* images:**  
 * images 1 + 2:  
![background1](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img1_backyard1.png)  
 * images 2 + 3:  
![background2](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img2_backyard2.png)  

2.	**Panorama output images (*Examples* folder):**	  
![background](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img3_backyard.png)  
![office](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img4_office.png)  
![oxford](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img5_oxford.png)  

3. **Panorama output images (*Mine* folder):**  
![view](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img6_m.jpg)   
![room](https://github.com/Kineruth/Panorama_Stitching/blob/master/data/Readme%20Images/img7_room.jpg)   
