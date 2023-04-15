#!/usr/bin/env python
# //==============================================================================
# /*
#     Software License Agreement (BSD License)
#     Copyright (c) 2021

#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:

#     * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.

#     * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.

#     * Neither the name of authors nor the names of its contributors may
#     be used to endorse or promote products derived from this software
#     without specific prior written permission.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.

#     \author    <amunawar@jhu.edu>
#     \author    Adnan Munawar
#     \version   1.0
# */
# //==============================================================================
import nrrd
import PIL.Image
import numpy as np
from argparse import ArgumentParser
from natsort import natsorted
import sys
import os
import cv2

def save_image(array, im_name):
	im = PIL.Image.fromarray(array.astype(np.uint8))
	im.save(im_name)


def normalize_data(data):
	max = data.max()
	min = data.min()
	normalized_data = (data - min) / float(max - min)
	return normalized_data


def scale_data(data, scale):
	scaled_data = data * scale
	return scaled_data


def save_volume_as_images(data, im_prefix):
	for i in range(data.shape[2]):
		im_name = im_prefix + '0' + str(i) + '.png'
		save_image(data[:, :, i], im_name)


def deleteBackground(file_dir):
	files = natsorted(os.listdir(file_dir))
	# Read the image
	for file in files:
		src = cv2.imread(os.path.join(file_dir, file), 1)
	# Convert image to image gray
		tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	# Applying thresholding technique
		_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

	# Using cv2.split() to split channels 
		# of coloured image
		b, g, r = cv2.split(src)

		# Channels and alpha
		# b = b+18
		# g = g+153
		# r = r+255
		b = b+211
		g = g+211
		r = r+211
		rgba = [b, g, r, alpha]
		
		# Using cv2.merge() to merge rgba
		# into a coloured/multi-channeled image
		dst = cv2.merge(rgba, 4)
		# Writing and saving to a new image
		cv2.imwrite(os.path.join(file_dir, file), dst)

def main():
	# Begin Argument Parser Code
	parser = ArgumentParser()
	parser.add_argument('-n', action='store', dest='nrrd_file', help='Specify Nrrd File')
	parser.add_argument('-p', action='store', dest='image_prefix', help='Specify Image Prefix',
						default='plane0')

	parsed_args = parser.parse_args()
	print('Specified Arguments')
	print(parsed_args)

	data, header = nrrd.read(parsed_args.nrrd_file)
	file_dir = parsed_args.image_prefix[:-7]
	normalized_data = normalize_data(data)
	scaled_data = scale_data(normalized_data, 255.9)
	save_volume_as_images(scaled_data, parsed_args.image_prefix)
	deleteBackground(file_dir)

if __name__ == '__main__':
    main()
