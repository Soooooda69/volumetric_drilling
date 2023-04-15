# Import the library OpenCV

import cv2
import sys
import os
from natsort import natsorted
  # Import the image

file_dir = sys.argv[1]
files = natsorted(os.listdir(file_dir))
  # Read the image
for file in files:
    src = cv2.imread(os.path.join(file_dir, file), 1)
  # Convert image to image gray

    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

  # Applying thresholding technique

    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    # print(alpha.shape, alpha)

  # Using cv2.split() to split channels 

    # of coloured image

    b, g, r = cv2.split(src)

    # Making list of Red, Green, Blue

    # Channels and alpha
    # b = b+18
    # g = g+153
    # r = r+255
    rgba = [b, g, r, alpha]
    
    # Using cv2.merge() to merge rgba

    # into a coloured/multi-channeled image

    dst = cv2.merge(rgba, 4)
    # Writing and saving to a new image

    cv2.imwrite(os.path.join(file_dir, file), dst)
