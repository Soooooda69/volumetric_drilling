#!/usr/bin/env python

import os
import numpy as np
import rospy
import message_filters
from argparse import ArgumentParser
import sys
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
from scipy.spatial.transform import Rotation as R
from cv_bridge import CvBridge
import cv2
bridge = CvBridge()
import time
import json
from ambf_msgs.msg import ObjectState, RigidBodyCmd, CameraCmd


global cam_xyz_offset
cam_xyz_offset = np.zeros([3,1])

def move(drill_pose, drill_Cmd):
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
    conversion = 0.180
    ## Get the rotation
    drill_r = R.from_matrix(drill_pose[:3,:3])

    ## Convert rotation to quaternion
    drill_quat = drill_r.as_quat()

    ## Get the translation in mm
    drill_t = drill_pose[:3,3]/conversion/1000

    ## update the command of drill
    drill_Cmd.pose.position.x = drill_t[0]
    drill_Cmd.pose.position.y = drill_t[1]
    drill_Cmd.pose.position.z = drill_t[2]
    drill_Cmd.pose.orientation.x = drill_quat[0]
    drill_Cmd.pose.orientation.y = drill_quat[1]
    drill_Cmd.pose.orientation.z = drill_quat[2]
    drill_Cmd.pose.orientation.w = drill_quat[3]

    return drill_Cmd


def invTransformation(trans):
        '''
        Inverse of the SE(3) transformation.
        '''
        R = trans[:3, :3]
        t = trans[:3, 3].reshape(3, 1)
        R_new = R.T
        t_new = -R.T@t
        inv_trans = np.vstack((np.hstack((R_new, t_new)), np.array([0,0,0,1])))
        return inv_trans


def rosmsg2quat(msg):
        '''
        transfer a rosmsg pose to seven params.
        '''
        t_x = msg.pose.position.x 
        t_y = msg.pose.position.y 
        t_z = msg.pose.position.z 
        x = msg.pose.orientation.x
        y = msg.pose.orientation.y
        z = msg.pose.orientation.z
        w = msg.pose.orientation.w
        conv_quat = [t_x,t_y,t_z,x,y,z,w]
        return conv_quat


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


def calculate_transformation(drill_pose, pan_pose):
    '''
    Calculate the target transformation with the rosmsg poses.
    '''
    ## convert quaternion to 4x4 transformation matrix 
    T_o_db = quat2trans(rosmsg2quat(drill_pose))
    T_o_pb = quat2trans(rosmsg2quat(pan_pose))
    
    ## by annotating F_A_B means transformation of B w.r.t A

    T_o_d = T_o_db@T_db_d
    # Fix the phacon to AMBF origin
    T_o_p = T_o_pb@T_pb_p
    T_p_o = invTransformation(T_o_p)
    
    # Get the camera and drill poses w.r.t the phantom
    T_p_d = T_p_o@T_o_d
    return T_p_d


def callback(*publishers):

    global cam_xyz_offset
    global pub_drill, pub_camera, pub_limage, pub_eval_image, args


    [drill_pose, pan_pose] = publishers 


    drill_cmd = RigidBodyCmd()
    cam_cmd = CameraCmd()
    drill_cmd.cartesian_cmd_type = 1
    cam_cmd.enable_position_controller = 1

    T_p_d = calculate_transformation(drill_pose, pan_pose)
    drill_cmd = move(T_p_d, drill_cmd)

    # publish topics
    pub_drill.publish(drill_cmd)

    # visualize 
    spinner_char = spinner[rospy.Time.now().secs % len(spinner)]
    print(f"Moving... {spinner_char}", end="\r")


def my_shutdown_hook():
    print("in my_shutdown_hook")


def main():
    global pub_drill, pub_camera, pub_pose_pan, pub_pose_drill, pub_pose_camhand, cam_mtx, args, X, R_db_d, T_pb_p, T_db_d, msg, spinner
    spinner = ['-', '\\', '|', '/']

    # Load the calibration parameters
    f = open(args.config)
    calib_config_path = json.load(f)
    
    cam_mtx = np.load(calib_config_path['root_path']+calib_config_path['camera_matrix'])
    X = np.load(calib_config_path['root_path']+calib_config_path['T_cb_c'])
    t_db_d = np.load(calib_config_path['root_path']+calib_config_path['t_db_d'])
    R_db_d =np.load(calib_config_path['root_path']+calib_config_path['R_db_d'])
    T_db_d = np.vstack([np.hstack([R_db_d, t_db_d]),np.array([0,0,0,1]).reshape(1,4)])
    T_p_pb = np.load(calib_config_path['root_path']+calib_config_path['T_p_pb'])
    T_pb_p = invTransformation(T_p_pb)
    
    # Initialize ROS node
    rospy.init_node('image_extract_node', anonymous=True)

    # Subscribers
    pose_pan_sub = message_filters.Subscriber('fwd_pose_pan', PoseStamped)
    pose_drill_sub = message_filters.Subscriber('fwd_pose_drill', PoseStamped)

    ##Publishers
    pub_drill = rospy.Publisher('/ambf/env/mastoidectomy_drill/Command',RigidBodyCmd, tcp_nodelay=True, queue_size=10)
    pub_camera = rospy.Publisher('/ambf/env/cameras/main_camera/Command',CameraCmd, tcp_nodelay=True, queue_size=10)

    ts = message_filters.ApproximateTimeSynchronizer([pose_drill_sub, pose_pan_sub], 50, 0.5)
    ts.registerCallback(callback)

    rospy.spin()
    rospy.on_shutdown(my_shutdown_hook)

    
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-c", "--config", required=False, type=str, help="Configuration file containing paths of all calibration parameters.")
    args = parser.parse_args()
    
    main()