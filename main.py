import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from moviepy.editor import VideoFileClip
from helpers import *

images = os.listdir("test_images/")

for image_name in images:
    image = mpimg.imread('test_images/' + image_name)
    
    # Convert to grayscale and smooth
    gray = grayscale(image)
    blur_gray = gaussian_blur(gray, 3)

    # Apply Canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = canny(blur_gray, low_threshold, high_threshold)

    # Find region of interest
    sizey = image.shape[0]
    sizex = image.shape[1]
    vertices = np.array([[(0,sizey),(470, 320), (490, 320), (sizex,sizey)]], dtype=np.int32)
    roi = region_of_interest(edges, vertices)

    # Apply Hough line detection
    rho = 2
    theta = np.pi/180
    threshold = 15
    min_line_length = 25
    max_line_gap = 10
    lines = hough_lines(roi, rho, theta, threshold, min_line_length, max_line_gap)

    # Add Hough lines to image
    result = weighted_img(lines, image)

    # Save image
    mpimg.imsave('test_images_output/out_' + image_name, result)

white_output = 'test_videos_output/solidWhiteRight.mp4'
##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image)
white_clip.write_videofile(white_output, audio=False)

yellow_output = 'test_videos_output/solidYellowLeft.mp4'
##clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4').subclip(0,5)
clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4')
yellow_clip = clip2.fl_image(process_image)
yellow_clip.write_videofile(yellow_output, audio=False)