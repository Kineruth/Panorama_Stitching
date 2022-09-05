**Date: 9/10/2019**  
**Last Edit: 05/09/2022**

Panorama Registration & Stitching
===

**Project source can be downloaded from:**
https://github.com/Kineruth/Panorama_Stitching  
This is a final project for Image Processing course at Ariel University. 

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
The human visual system has a field of view of around $135 x 200$ degrees, but a typical camera has a field of view of only $35 x  50$ degrees. Therefore, panoramic image mosaicking works by taking lots of pictures from an ordinary camera and stitching them together to form a composite image with a much larger field of view.   
The quality of image stitching is measured by the similarity of the stitched image to each of the input images. It also can be measured by the visibility of the seam between the stitched images.  

**Approach And Method**
==

Resignation:
--
* ***Feature Extraction (SIFT):***  
For each pair of consecutive frames in our image sequence, we use *scale-invariant feature transform* (SIFT) to detect and describe local features between them. SIFT enables reliable image matching with various orientation and zoom. The basic steps of the extraction algorithm are Scale-space extrema detection, keypoint localization, orientation assignment and keypoint descriptor. 
* ***Feature matching (BF):***  
 After finding all feature points in both images, we use Brute-Force Matcher to match those feature points to each other.   
The algorithm runs over each keypoint $K_1$ from the first set (image1), takes every keypoint in the second set (image2) and calculates the distance between them. The keypoint that produced the smallest distance will be considered its pair ( $K_1$ , $K_2$). The algorithm returns a set of all matched keypoints. 
* ***Registering the transformation:***  
When matching the SIFT feature points using BF, there will be lots of mismatches. The RANSAC algorithm can be used to remove the mismatches by finding the transformation matrix of these feature points.    
**RANSAC (RANdom  SAmple Consensus)** is a non-deterministic algorithm because it doesn’t ensure to return acceptable results. It is used to estimate parameters for the Homography of a mathematical model from a set of observed data that contains outliers iteratively.    

RANSAC  loop involves:
1. selects four random feature pairspoint.  
2. computes their homography $H$ using least square (SVD composition).  
3. computes estimated points of the second frame using the homography $H$ that was calculated.   
4. computes inliers: if $E_j = || P'_1,j - P_2,j || < inlierTol$  where $j=1..N$ and *inlierTol = some constant threshold*, then it is added as an inlier.  
5. keeps the largest set of inliers and its homography $H$.  
When finished, RANSAC will return the maximum set of inliers found between each pair of frames and the transformation matrix of its feature points.  
We chose $inlierTol = 10$ because we saw it gives a good amount of inliers sets - quite a bit and not much either. 

Panorama Stitching:
--
* ***Transforming into a common coordinate system:***  
We need to choose a coordinate system in which we would like the panorama to be rendered. We chose it to be the coordinate system of the middle frame $I_m$ in our image sequence and transformed all other frames to that coordinate system.   
The resulting panorama image will have a frame $I_m$ coordinate system and be composed of all the transformed frames back-warped so that they properly align with it.  

* ***Rendering the panorama:***  
So far, we have $H_{tot}$ that is a set of $M$ homographies $\tilde{H_{i,m}}$ where $i=1..M$ and *M = the amount of frames*, that transforms pixel coordinates in frame $I_i$ to the panorama coordinate system.      
First, we need to define where we want the panorama image $I_{pano}$ to be rendered. We would like this region to be large enough to include all pixels from all frames. For that, we define which parts of $I_{pano}$ should be obtained from each frame $I_i$.   
We divide the panorama to $M$ vertical strips and finally, we Back-Warp the images on the strips of the panorama using $H_{tot}$.  
We did not succeed implementing the way was instructed, so we used opencv function wrapPerspective.  

Results
==

The experiments we have done:
--
* ***findFeatures -***   We debated between SURF and SIFT algorithms and decided to go with SIFT because people say it is more used for implementing finding features in image stitching.   
* ***matchFeatures -***   At first, we matched descriptor vectors with a *Flann based Matcher*, but saw that it does not return accurate matched values, so we switched to *Brute-Force Matcher* and it gave much more accurate results.   
* ***Choosing threshold (inlierTol) -***   We ran our implementation on our input pictures:  
1. for $threshold = 5$ →  got around $115$ inliers.   
2. for $threshold = 10$ →  got around $110~120$ inliers.  
3. for $threshold = 20$ →  got around $120~130$ inliers.  
So we used $threshold = 10$ because it looked the most accurate for the eye.  

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
