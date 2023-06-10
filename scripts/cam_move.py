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
from scipy.spatial.transform import Rotation as R
from cv_bridge import CvBridge
import cv2
bridge = CvBridge()
import json
from ambf_msgs.msg import ObjectState, RigidBodyCmd, CameraCmd

sys.path.append('/home/shc/Twin-S/util')
from Solver import solver
sol = solver()

def move(drill_pose, cam_pose, drill_Cmd, cam_Cmd):
    '''
    Get the tracking poses of drill and camera, update to ambf. 
    Args:
    - drill_pose (4x4, numpy array): transformation matrix [R, t]
    - cam_pose (4x4, numpy array): transformation matrix [R, t]
    - drill_Cmd: RigidBodyCmd
    - cam_Cmd: CameraCmd

    Returns:
    - drill_Cmd: RigidBodyCmd
    - cam_Cmd: CameraCmd
    '''
    conversion = 0.180 # 1AU = 0.18m
    ## Get the rotation
    drill_r = R.from_matrix(drill_pose[:3,:3])
    cam_r = R.from_matrix(cam_pose[:3,:3])

    ## Convert rotation to quaternion
    drill_quat = drill_r.as_quat()
    cam_quat = cam_r.as_quat()

    ## Get the translation in ambf units
    drill_t = drill_pose[:3,3]/conversion/1000
    cam_t = cam_pose[:3,3]/conversion/1000

    ## update the command of drill and camera
    cam_Cmd.pose.position.x = cam_t[0]
    cam_Cmd.pose.position.y = cam_t[1]
    cam_Cmd.pose.position.z = cam_t[2]
    cam_Cmd.pose.orientation.x = cam_quat[0]
    cam_Cmd.pose.orientation.y = cam_quat[1]
    cam_Cmd.pose.orientation.z = cam_quat[2]
    cam_Cmd.pose.orientation.w = cam_quat[3]
    
    return drill_Cmd, cam_Cmd


def quat2trans(quat):
    """
    Quaternion to 4x4 transformation.
    
    Args:
    - quat (4, numpy array): quaternion w, x, y, z
    Returns:
    - rotm: (4x4 numpy array): transformation matrix
    """
    x = quat[3]
    y = quat[4]
    z = quat[5]
    w = quat[6]

    t_x = quat[0]*1000
    t_y = quat[1]*1000
    t_z = quat[2]*1000

    s = w*w + x*x + y*y + z*z

    homo = np.array([[1-2*(y*y+z*z)/s, 2*(x*y-z*w)/s,   2*(x*z+y*w)/s  ,t_x],
                     [2*(x*y+z*w)/s,   1-2*(x*x+z*z)/s, 2*(y*z-x*w)/s  ,t_y],
                     [2*(x*z-y*w)/s,   2*(y*z+x*w)/s,   1-2*(x*x+y*y)/s, t_z],
                     [0,0,0,1]
    ])

    return homo

def calculate_transformation(camhand_pose, pan_pose):
    ## convert quaternion to 4x4 transformation matrix 
    T_o_cb = quat2trans(sol.rosmsg2quat(camhand_pose))

    T_o_pb = quat2trans(sol.rosmsg2quat(pan_pose))

    ## by annotating A2B means transformation of B w.r.t A or F_A_B
    ## F_o_cam = F_o_camhand * X
    T_o_c = T_o_cb @ T_cb_c

    ## F_cv_ambf
    extrinsic = np.array([[0, 1, 0, 0], [0, 0, -1, 0],
                          [-1, 0, 0, 0], [0, 0, 0, 1]])

    

    # Fix the phacon to AMBF origin
    T_o_p = T_o_pb@T_pb_p
    T_p_o = sol.invTransformation(T_o_p)
    T_p_c = T_p_o@T_o_c@extrinsic
    return T_p_c

def callback(*publishers):
    global cam_xyz_offset
    '''
    Args:
    - camhand_pose : pose msg of camera hand in tracker coordinate
    - drill_pose : pose msg of drill in tracker coordinate
    '''
    global pub_camera, pub_limage, pub_eval_segm, pub_pointcloud, args

    if args.eval_segm:
        [camhand_pose, pan_pose, limage, segm] = publishers
    elif args.sync_pcd:
        [camhand_pose, pan_pose, limage, pcd] = publishers
    else:
        [camhand_pose, pan_pose, limage] = publishers


    drill_cmd = RigidBodyCmd()
    cam_cmd = CameraCmd()
    cam_cmd.enable_position_controller = 1
 
    T_p_c = calculate_transformation(camhand_pose, pan_pose)
    drill_cmd, cam_cmd = move(np.eye(4), T_p_c, drill_cmd, cam_cmd)

    # visualize 
    spinner_char = spinner[rospy.Time.now().secs % len(spinner)]
    print(f"Cam Moving... {spinner_char}", end="\r")
    
    pub_camera.publish(cam_cmd)
    # print(T_p_c[:3, 3].T)

    if args.sim_sync:
        limage.header.stamp = rospy.Time.now()
        pan_pose.header.stamp = rospy.Time.now()
        camhand_pose.header.stamp = rospy.Time.now()
        pub_limage.publish(limage)
        pub_pose_pan.publish(pan_pose)
        pub_pose_camhand.publish(camhand_pose)
        if args.sync_pcd:
            pcd.header.stamp = rospy.Time.now()
            pub_pointcloud.publish(pcd)

    if args.eval_segm:
        limage.header.stamp = rospy.Time.now()
        segmimg_arr = np.fromstring(segm.data, np.uint8)
        segm_image = cv2.imdecode(segmimg_arr, cv2.IMREAD_COLOR)

        limg_arr = np.fromstring(limage.data, np.uint8)
        limg_image = cv2.imdecode(limg_arr, cv2.IMREAD_COLOR)
        l_image = cv2.resize(limg_image, (640, 360))
        overlap = cv2.addWeighted(l_image, 0.5, segm_image, 0.5, 0)

        #### Create eval CompressedImage topic ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', overlap)[1]).tostring()
        # Publish new image
        pub_eval_segm.publish(msg)


def my_shutdown_hook():
    print("in my_shutdown_hook")


def cam_offset_cb(msg):
    global cam_xyz_offset
    cam_xyz_offset[0] = msg.data[0]
    cam_xyz_offset[1] = msg.data[1]
    cam_xyz_offset[2] = msg.data[2]


def main():
    global pub_camera, cam_mtx, pub_eval_segm, pub_limage, pub_pose_pan, pub_pose_camhand, pub_pointcloud, T_cb_c, T_pb_p, spinner
    spinner = ['-', '\\', '|', '/']

    f = open(args.config)
    calib_config_path = json.load(f)
    
    cam_mtx = np.load(calib_config_path['root_path']+calib_config_path['camera_matrix'])
    T_cb_c = np.load(calib_config_path['root_path']+calib_config_path['T_cb_c'])
    T_p_pb = np.load(calib_config_path['root_path']+calib_config_path['T_p_pb'])
    T_pb_p = sol.invTransformation(T_p_pb)

    # Initialize ROS node
    rospy.init_node('image_extract_node', anonymous=True)

    # Subscribers
    limage_sub = message_filters.Subscriber('fwd_limage/compressed', CompressedImage)
    pose_pan_sub = message_filters.Subscriber('fwd_pose_pan', PoseStamped)
    pose_camhand_sub = message_filters.Subscriber('fwd_pose_camhand', PoseStamped)
    pointcloud_sub = message_filters.Subscriber('fwd_pointcloud', PointCloud2)

    # pub_eval_image = rospy.Publisher('/eval_drill/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
    # pub_drill = rospy.Publisher('/ambf/env/mastoidectomy_drill/Command',RigidBodyCmd, tcp_nodelay=True, queue_size=10)
    pub_camera = rospy.Publisher('/ambf/env/cameras/main_camera/Command',CameraCmd, tcp_nodelay=True, queue_size=10)
    if args.sim_sync:
        pub_limage = rospy.Publisher('/pss_limage/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
        pub_pose_pan = rospy.Publisher('/pss_pose_pan',PoseStamped, tcp_nodelay=True, queue_size=10)
        pub_pose_camhand = rospy.Publisher('/pss_pose_camhand',PoseStamped, tcp_nodelay=True, queue_size=10)
        if args.sync_pcd:
            pub_pointcloud = rospy.Publisher('/pss_pointcloud',PointCloud2, tcp_nodelay=True, queue_size=10)
            ts = message_filters.ApproximateTimeSynchronizer([pose_camhand_sub, pose_pan_sub, limage_sub, pointcloud_sub], 50, 0.5)
            ts.registerCallback(callback)

    if args.eval_segm:
        segm_sub = message_filters.Subscriber('/ambf/env/cameras/main_camera/ImageData/compressed', CompressedImage) ##'/ambf/env/cameras/segmentation_camera/ImageData/compressed'
        pub_eval_segm = rospy.Publisher('/eval_segm/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
        ts = message_filters.ApproximateTimeSynchronizer([pose_camhand_sub, pose_pan_sub, limage_sub, segm_sub], 50, 0.5)
        ts.registerCallback(callback)
    else:
        ts = message_filters.ApproximateTimeSynchronizer([pose_camhand_sub, pose_pan_sub, limage_sub], 50, 0.5)
        ts.registerCallback(callback)

    rospy.spin()

    rospy.on_shutdown(my_shutdown_hook)


if __name__ == '__main__':

    parser = ArgumentParser()
    # parser.add_argument("--handeye", dest="X_path", help="path of handeye transformation X", default='hand_eye_X.npy', type=str)
    parser.add_argument("--eval_segm", dest='eval_segm', help='pulish images to evaluate the overlay of segmentation mask and the real scene.', action='store_true')
    parser.add_argument("--sim_sync", dest='sim_sync', help='sync the recorded images with the sim scene.', action='store_true')
    parser.add_argument("--pcd", dest='sync_pcd', help='sync the recorded pointcloud from camera.', action='store_true')
    parser.add_argument("-c", "--config", required=False, type=str, help="Configuration file containing paths of all calibration parameters.")
    args = parser.parse_args()
    
    main()
