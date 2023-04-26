#!/usr/bin/env python

import os
import numpy as np
import rospy
import ros_numpy
import message_filters
from argparse import ArgumentParser
import sys
from sensor_msgs.msg import CompressedImage, Image, PointCloud2
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from scipy.spatial.transform import Rotation as R
from cv_bridge import CvBridge
import cv2
bridge = CvBridge()
from ambf_client import Client
import time
from ambf_msgs.msg import ObjectState, RigidBodyCmd, CameraCmd
import matplotlib as mpl
import open3d as o3d
import matplotlib.pyplot as plt
sys.path.insert(0, '/home/shc/Twin-S/util')
from ros_tools import rostools
rt = rostools()


def callback(pss_limage, segm, pcd):
    '''
    Args:
    - camhand_pose : pose msg of camera hand in tracker coordinate
    - drill_pose : pose msg of drill in tracker coordinate
    '''
    global pub_eval_segm
    pss_limage.header.stamp = rospy.Time.now()
    segmimg_arr = np.fromstring(segm.data, np.uint8)
    segm_image = cv2.imdecode(segmimg_arr, cv2.IMREAD_COLOR)

    limg_arr = np.fromstring(pss_limage.data, np.uint8)
    l_image = cv2.imdecode(limg_arr, cv2.IMREAD_COLOR)

    # cv2.imwrite(f'eval_images/ZEDRGB_{pss_limage.header.stamp}.png', limg_image)
    # cv2.imwrite(f'eval_images/AMBFSegm_raw_{pss_limage.header.stamp}.png', segm_image)
    # cv2.imwrite(f'eval_images/AMBFSegm_modified_{pss_limage.header.stamp}.png', rec_segm_image)


    l_image = cv2.resize(l_image, (640, 360))
    # segm_image = cv2.resize(segm_image, (1920, 1080))
    overlap = cv2.addWeighted(l_image, 0.5, segm_image, 0.5, 0)
    # overlap = rec_segm_image
    #### Create eval CompressedImage topic ####
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    msg.data = np.array(cv2.imencode('.jpg', overlap)[1]).tostring()
    # Publish new image
    pub_eval_segm.publish(msg)
    print('Eval images published!')


def my_shutdown_hook():
    print("in my_shutdown_hook")


def main():
    global pub_eval_segm

    # Initialize ROS node
    rospy.init_node('image_extract_node', anonymous=True)

    # Subscribers
    pss_limage_sub = message_filters.Subscriber('pss_limage/compressed', CompressedImage)
    segm_sub = message_filters.Subscriber('/ambf/env/cameras/segmentation_camera/ImageData/compressed', CompressedImage)
    pcd_sub = message_filters.Subscriber('/ambf/env/cameras/main_camera/DepthData', PointCloud2)   

    pub_eval_segm = rospy.Publisher('/eval_segm/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
    ts = message_filters.ApproximateTimeSynchronizer([pss_limage_sub, segm_sub, pcd_sub], 50, 0.5)
    ts.registerCallback(callback)

    rospy.spin()

    rospy.on_shutdown(my_shutdown_hook)


if __name__ == '__main__':
    
    main()
