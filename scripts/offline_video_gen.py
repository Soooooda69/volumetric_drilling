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


def callback(sim, segm):
    '''
    Args:
    - camhand_pose : pose msg of camera hand in tracker coordinate
    - drill_pose : pose msg of drill in tracker coordinate
    '''
    global videoWriter1, videoWriter2
    segmimg_arr = np.frombuffer(segm.data, np.uint8)
    segm_image = cv2.imdecode(segmimg_arr, cv2.IMREAD_COLOR)

    simimg_arr = np.frombuffer(sim.data, np.uint8)
    sim_image = cv2.imdecode(simimg_arr, cv2.IMREAD_COLOR)

    spinner_char = spinner[rospy.Time.now().secs % len(spinner)]
    print(f"                                  recording video frames... {spinner_char}", end="\r")
    
    videoWriter1.write(sim_image)
    videoWriter2.write(segm_image)


def my_shutdown_hook():
    videoWriter1.release()
    videoWriter2.release()
    print("in my_shutdown_hook")


def main():
    global videoWriter1,videoWriter2, spinner
    spinner = ['-', '\\', '|', '/']

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 15
    size = (640, 360)
    num1= 'gt_t'
    videoWriter1 = cv2.VideoWriter(f'/media/shc/Elements/Twin-S_data/{num1}.mp4', fourcc, fps, size)
    num2 = 'rgb'
    videoWriter2 = cv2.VideoWriter(f'/media/shc/Elements/Twin-S_data/{num2}.mp4', fourcc, fps, size)

    # Initialize ROS node
    rospy.init_node('image_extract_node', anonymous=True)

    # Subscribers
    # segm_sub = message_filters.Subscriber('/ambf/env/cameras/main_camera/ImageData/compressed', CompressedImage)
    sim_sub = message_filters.Subscriber('/ambf/env/cameras/stereoL/ImageData/compressed', CompressedImage)   
    segm_sub = message_filters.Subscriber('/fwd_limage/compressed', CompressedImage)
    ts = message_filters.ApproximateTimeSynchronizer([sim_sub, segm_sub], 50, 0.5)
    ts.registerCallback(callback)

    rospy.spin()

    rospy.on_shutdown(my_shutdown_hook)


if __name__ == '__main__':
    
    main()
