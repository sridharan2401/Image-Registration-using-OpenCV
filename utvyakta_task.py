# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:44:00 2020

@author: Sridharan
"""

import cv2 
import numpy as np
import glob

def transform(testimage,originalimage):
    # Convert to grayscale. 
    test_image = cv2.cvtColor(testimage, cv2.COLOR_BGR2GRAY) 
    original_image = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY) 
    height, width = original_image.shape 
    
    # Creating ORB detector  
    orb_detector = cv2.ORB_create() 
    
    #keypoints and descriptors
    kp1, d1 = orb_detector.detectAndCompute(test_image, None) 
    kp2, d2 = orb_detector.detectAndCompute(original_image, None) 
    
    # Brute Force matcher with Hamming distance
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 
    
    # Matching descriptors 
    matches = matcher.match(d1, d2) 
    
    # sorting matches 
    matches.sort(key = lambda x: x.distance) 
    
    #selecting top 90% matches 
    matches = matches[:int(len(matches)*90)] 
    no_of_matches = len(matches) 
    
    drawmatches = cv2.drawMatches(testimage,kp1,originalimage,kp2,matches,None)
    
    #empty matrices of shape no_of_matches * 2 
    p1 = np.zeros((no_of_matches, 2)) 
    p2 = np.zeros((no_of_matches, 2)) 
    
    for i in range(len(matches)): 
        p1[i, :] = kp1[matches[i].queryIdx].pt 
        p2[i, :] = kp2[matches[i].trainIdx].pt 
    
    #homography matrix 
    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC) #homography using Random sample consensus
    
    #print(homography)
    # transforming image using homography 
    transformed_img = cv2.warpPerspective(test_image_color, 
    					homography, (width, height)) 
    return transformed_img,drawmatches

ORIGINAL_PATH = 'Original\\'

TEST_PATH = 'Test_images\\'

if __name__ == '__main__':
    #Opening original image 
    original_image_color = cv2.imread(ORIGINAL_PATH+'original.jpg') #Original image. 
    
    images = glob.glob(TEST_PATH + '*.jpg')
    
    img = 1
    for image in images:
        test_image_color = cv2.imread(image) # Image to be transformed.
        
        transformed_img, draw_matches = transform(test_image_color,original_image_color)
        
        output_image = 'Transformed/transformed'+str(img)+'.jpg'
        matched ='Matched/matched'+str(img)+'.jpg'
        # writing transformed image 
        cv2.imwrite(output_image, transformed_img) 
        cv2.imwrite(matched,draw_matches)
        img += 1
