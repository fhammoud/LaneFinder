# **Finding Lane Lines on the Road** 


**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps:

  * Convert the images to grayscale
  * Apply Canny to find all the edges
  * Mask a region of interest around the lanes
  * Apply Hough function to find all the lines in the ROI
  * Add Hough lines to the image

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by separating the left and right lines the Hough function returns by calculating their slopes using (y2-y1)/(x2-x1). Positive values were right lines and negative values were left. I also filtered the lines using a range of slopes to try and ignore any horizontal lines. Once I had the lines I want I calculated their average positions to get a single line for the left and right lane lines. These lines represent the average position and slope of all the left and right lines. To extend these lines I was able to take the two lines and calculate the y-intercept using b=y-mx since I had m,x and y. Once I had b I found the two endpoints of the solid lines I need by using x=(y-b)/m, plugging in 540 and 320 as the y positions.


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when the lane lines are not clearly marked or do not exist? Finding the average single lines would crash the program with a divide by zero error.

Another shortcoming could be if the resolution of the image is different. I would get a bad looking region of interest and solid lines because I am hardcoding the number of pixels I want.


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to calculate the vertices and limits of my lines in a more robust manner that is independent of resolution.

Another potential improvement could be to find a way to make the solid lines look less jittery in the video.