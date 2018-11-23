import numpy as np
# from cv import cv2 as cv
import cv2 as cv

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv.imread()
    # return cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    left_count = 0
    left_x1_sum = 0
    left_y1_sum = 0
    left_x2_sum = 0
    left_y2_sum = 0
    right_count = 0
    right_x1_sum = 0
    right_x2_sum = 0
    right_y1_sum = 0
    right_y2_sum = 0
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            
            # Separate left and right lines and ignore nay horizontal lines
            slope = (y2-y1)/(x2-x1)
            if 0.8 > slope > 0.4:
                # right line
                right_count += 1
                right_x1_sum += x1
                right_x2_sum += x2
                right_y1_sum += y1
                right_y2_sum += y2
            elif -0.9 < slope < -0.5:
                # left line
                left_count += 1
                left_x1_sum += x1
                left_x2_sum += x2
                left_y1_sum += y1
                left_y2_sum += y2
    
    # Find average position for left and right lines
    left_x1 = left_x1_sum/left_count
    left_y1 = left_y1_sum/left_count
    left_x2 = left_x2_sum/left_count
    left_y2 = left_y2_sum/left_count

    right_x1 = right_x1_sum/right_count
    right_y1 = right_y1_sum/right_count
    right_x2 = right_x2_sum/right_count
    right_y2 = right_y2_sum/right_count

    # Find slopes of left and right lines
    left_slope = (left_y2 - left_y1) / (left_x2 - left_x1)
    right_slope = (right_y2 - right_y1) / (right_x2 - right_x1)

    # Find y-intercepts of left and right lines
    left_b = left_y1 - left_slope * left_x1
    right_b = right_y1 - right_slope * right_x1

    # Find new points of extended left and right lines
    left_line_x1 = int(round((540 - left_b)/left_slope))
    left_line_y1 = 540
    left_line_x2 = int(round((330 - left_b)/left_slope))
    left_line_y2 = 330

    right_line_x1 = int(round((540 - right_b)/right_slope))
    right_line_y1 = 540
    right_line_x2 = int(round((330 - right_b)/right_slope))
    right_line_y2 = 330

    # Create left and right lines on the image
    cv.line(img, (left_line_x1,left_line_y1), (left_line_x2, left_line_y2), color, thickness)
    cv.line(img, (right_line_x1,right_line_y1), (right_line_x2,right_line_y2), color, thickness)
#     for line in lines:
#         for x1,y1,x2,y2 in line:
#             slope = (y2-y1)/(x2-x1)
#             print(slope)
#             cv.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv.addWeighted(initial_img, α, img, β, γ)

def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    
    # Convert to grayscale and smooth
    gray = grayscale(image)
    blur_gray = gaussian_blur(gray, 5)

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
    min_line_length = 20
    max_line_gap = 10
    lines = hough_lines(roi, rho, theta, threshold, min_line_length, max_line_gap)

    # Add Hough lines to image
    result = weighted_img(lines, image)

    return result