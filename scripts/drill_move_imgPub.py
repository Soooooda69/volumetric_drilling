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
from ambf_object import Object
from ambf_msgs.msg import ObjectState, RigidBodyCmd, CameraCmd
from std_msgs.msg import Float32MultiArray


sys.path.insert(0, '/home/shc/Twin-S/util')
from Solver import solver
from dataLoader import dataLoader
sol = solver()
ld = dataLoader()

global cam_xyz_offset
cam_xyz_offset = np.zeros([3,1])

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
    conversion = 0.180
    ## Get the rotation
    drill_r = R.from_matrix(drill_pose[:3,:3])
    cam_r = R.from_matrix(cam_pose[:3,:3])

    ## Convert rotation to quaternion
    drill_quat = drill_r.as_quat()
    cam_quat = cam_r.as_quat()

    ## Get the translation in mm
    drill_t = drill_pose[:3,3]/conversion/1000
    cam_t = cam_pose[:3,3]/conversion/1000

    ## update the command of drill
    drill_Cmd.pose.position.x = drill_t[0]
    drill_Cmd.pose.position.y = drill_t[1]
    drill_Cmd.pose.position.z = drill_t[2]
    drill_Cmd.pose.orientation.x = drill_quat[0]
    drill_Cmd.pose.orientation.y = drill_quat[1]
    drill_Cmd.pose.orientation.z = drill_quat[2]
    drill_Cmd.pose.orientation.w = drill_quat[3]

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


def eval_drill_tip(T_c_d, ros_limg):
    global cam_mtx
    
    np_arr = np.fromstring(ros_limg.data, np.uint8)
    left_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    t_c_d = T_c_d[:3, 3].reshape(3,1)
    pix,val,dist = projectWithoutDistortion(cam_mtx, 1920, 1080, t_c_d)
    
    # print(pix,val,dist)
    imgpt = np.int32(pix).reshape(-1, 2)
    # print('imgpt:', imgpt[0])
    imgpt[0][0] = imgpt[0][0]
    imgpt[0][1] = imgpt[0][1]
    tip_point = (imgpt[0][0], imgpt[0][1])
    eval_image = cv2.circle(left_image, tip_point, 5, [0, 0, 255], thickness=5)
    eval_image = cv2.resize(eval_image, (640, 360))
    return eval_image


def projectWithoutDistortion(intrinsic_matrix, width, height, pts):
    """
    Projects a list of points to the camera defined transform, intrinsics and distortion
    :param intrinsic_matrix: 3x3 intrinsic camera matrix
    :param width: the image width
    :param height: the image height
    :param pts: a list of point coordinates (in the camera frame) with the following format
    :return: a list of pixel coordinates with the same lenght as pts
    """

    _, n_pts = pts.shape

    # Project the 3D points in the camera's frame to image pixels without considering the distorcion
    # From https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
    pixs = np.zeros((2, n_pts), dtype=float)

    # fx, _, cx, _, fy, cy, _, _, _ = intrinsic_matrix

    fx = intrinsic_matrix[0, 0]
    fy = intrinsic_matrix[1, 1]
    cx = intrinsic_matrix[0, 2]
    cy = intrinsic_matrix[1, 2]

    x = pts[0, :]
    y = pts[1, :]
    z = pts[2, :]

    dists = np.linalg.norm(pts[0:3, :], axis=0)  # compute distances from point to camera
    xl = np.divide(x, z)  # compute homogeneous coordinates
    yl = np.divide(y, z)  # compute homogeneous coordinates

    pixs[0, :] = fx * xl + cx
    pixs[1, :] = fy * yl + cy
    # Compute mask of valid projections
    valid_z = z > 0
    valid_xpix = np.logical_and(pixs[0, :] >= 0, pixs[0, :] < width)
    valid_ypix = np.logical_and(pixs[1, :] >= 0, pixs[1, :] < height)
    valid_pixs = np.logical_and(valid_z, np.logical_and(valid_xpix, valid_ypix))
    return pixs, valid_pixs, dists


# def callback(camhand_pose, drill_pose, pan_pose, limage):
def callback(*publishers):
    '''
    Args:
    - camhand_pose : pose msg of camera hand in tracker coordinate
    - drill_pose : pose msg of drill in tracker coordinate
    '''
    global cam_xyz_offset
    global pub_drill, pub_camera, pub_limage, pub_eval_image, args

    # [camhand_pose, drill_pose, pan_pose, limage] = publishers
    if args.eval_segm:
        [camhand_pose, drill_pose, pan_pose, limage, segm] = publishers
    else:
        [camhand_pose, drill_pose, pan_pose, limage, rimage] = publishers
    
    drill_cmd = RigidBodyCmd()
    cam_cmd = CameraCmd()
    drill_cmd.cartesian_cmd_type = 1
    cam_cmd.enable_position_controller = 1

    ## convert quaternion to 4x4 transformation matrix 
    T_o_cb = quat2trans(sol.rosmsg2quat(camhand_pose))
    T_o_db = quat2trans(sol.rosmsg2quat(drill_pose))
    T_o_pb = quat2trans(sol.rosmsg2quat(pan_pose))

    ## by annotating A2B means transformation of B w.r.t A or F_A_B
    ## F_o_cam = F_o_camhand * X
    T_o_c = np.dot(T_o_cb, X)

    T_c_o = sol.invTransformation(T_o_c) 

    ## F_cam_drill = F_cam_o * F_o_drill
    T_c_db =T_c_o@T_o_db

    ## T_db_d
    # R_db_d = np.eye(3)
    T_db_d = np.vstack([np.hstack([R_db_d, t_tip]),np.array([0,0,0,1]).reshape(1,4)])

    ## t_cam_tip = R_cam_drill * t_tip + t_cam_drill
    # t_c_d = np.dot(T_c_db[:3, :3], t_tip) + T_c_db[:3, 3].reshape(3,-1)
    T_c_d = T_c_db@T_db_d
    print("tip: ", T_c_d[:3, 3].reshape(-1,3))

    ## F_cam_tip = [R_cam_drill * R_drill_tip, t_cam_tip]
    T_o_d = T_o_db@T_db_d

    ## F_o_tip = [R_o_drill, t_o_tip]  This is most likely wrong!! Need R_drill_tip
    ## Update: F_o_tip = F_o_cam * F_cam_tip
    # op2tip = T_o_c @ T_c_d

    ## F_cv_ambf
    extrinsic = np.array([[0, 1, 0, 0], [0, 0, -1, 0],
                          [-1, 0, 0, 0], [0, 0, 0, 1]])

    ## F_o_ambf = F_o_cam * F_cv_ambf                    
    T_o_ambf = np.dot(T_o_c, extrinsic)
    T_ambf_o = sol.invTransformation(T_o_ambf)

    ## F_ambf_tip = F_ambf_op * F_o_tip
    # ambf2tip = np.dot(T_ambf_o, op2tip)

    ## R_ambf_tip = R_ambf_tip * R_offset
    # We would like to clarify that the calibration process is a requirement prior to running the digital twins system such that the virtual models can be aligned with the physical objects. Thus, the calibration process does not impact on the framerate of Twin-S after launching. The time spent for calibration is approximately 10 minutes The speed of Twin-S will be impacted by the speed of simulation, where the computational time breakdown is ???. We will add the above results and discussion to Appendix ???. 

    # Fix the phacon to AMBF origin
    T_o_p = T_o_pb@T_pb_p
    T_p_o = sol.invTransformation(T_o_p)

    # adjust the offset
    T_c_corr = np.identity(4)
    T_c_corr[0,3] = cam_xyz_offset[0]*1000
    T_c_corr[1,3] = cam_xyz_offset[1]*1000 
    T_c_corr[2,3] = cam_xyz_offset[2]*1000
    T_o_c = np.dot(T_o_c, T_c_corr)
    
    T_p_c = T_p_o@T_o_c
    T_p_d = T_p_o@T_o_d
    T_p_c = T_p_c@extrinsic
    drill_cmd, cam_cmd = move(T_p_d, T_p_c, drill_cmd, cam_cmd)

    # publish topics
    pub_drill.publish(drill_cmd)
    pub_camera.publish(cam_cmd)

    if args.sim_sync:
        limage.header.stamp = rospy.Time.now()
        rimage.header.stamp = rospy.Time.now()
        pan_pose.header.stamp = rospy.Time.now()
        camhand_pose.header.stamp = rospy.Time.now()
        drill_pose.header.stamp = rospy.Time.now()
        
        pub_limage.publish(limage)
        pub_rimage.publish(rimage)
        pub_pose_pan.publish(pan_pose)
        pub_pose_drill.publish(drill_pose)
        pub_pose_camhand.publish(camhand_pose)

    if args.eval_tip_rpj:
        # add the left image with evaluation circle 
        eval_limage = eval_drill_tip(T_c_d, limage)
        #### Create eval CompressedImage topic ####
        s = time.time()
        msg.data = np.array(cv2.imencode('.jpg', eval_limage)[1]).tostring()
        e = time.time()
        print(e-s)
        # Publish new image
        pub_eval_image.publish(msg)
        
    
    if args.eval_segm:
        limage.header.stamp = rospy.Time.now()
        segmimg_arr = np.fromstring(segm.data, np.uint8)
        segm_image = cv2.imdecode(segmimg_arr, cv2.IMREAD_COLOR)

        limg_arr = np.fromstring(limage.data, np.uint8)
        limg_image = cv2.imdecode(limg_arr, cv2.IMREAD_COLOR)
        l_image = cv2.resize(limg_image, (640, 360))
        overlap = cv2.addWeighted(l_image, 0.5, segm_image, 0.5, 0)

        #### Create eval CompressedImage topic ####
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
    global pub_drill, pub_camera, pub_limage,pub_rimage, pub_eval_image, pub_pose_pan, pub_pose_drill, pub_pose_camhand, pub_eval_segm, cam_mtx, args, X, t_tip, R_db_d, T_pb_p, msg

    cam_mtx = np.load('/home/shc/Twin-S/params/zed_M_l.npy')
    ## X: hand-eye transformation F_camhand_cam
    # argv[1]: X dir path
    X = np.load(args.X_path)

    ## Drill tip in drill coordinate t_tip from pivot calibration
    t_tip = np.load('/home/shc/Twin-S/params/drill_pivot_0425_.npy')

    ## Rotation of tip w.r.t drill marker got from rotation calibration
    R_db_d =np.load('/home/shc/Twin-S/params/R_db_d_.npy')

    ## Registration result
    T_p_pb = np.load('/home/shc/Twin-S/params/phacon2pan_0411.npy')
    T_pb_p = sol.invTransformation(T_p_pb)

    # Initialize ROS node
    rospy.init_node('image_extract_node', anonymous=True)

    # Define pub msg
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"

    # Subscribers
    limage_sub = message_filters.Subscriber('fwd_limage/compressed', CompressedImage)
    rimage_sub = message_filters.Subscriber('fwd_rimage/compressed', CompressedImage)
    pose_pan_sub = message_filters.Subscriber('fwd_pose_pan', PoseStamped)
    pose_drill_sub = message_filters.Subscriber('fwd_pose_drill', PoseStamped)
    pose_camhand_sub = message_filters.Subscriber('fwd_pose_camhand', PoseStamped)

    ##Publishers
    pub_drill = rospy.Publisher('/ambf/env/mastoidectomy_drill/Command',RigidBodyCmd, tcp_nodelay=True, queue_size=10)
    pub_camera = rospy.Publisher('/ambf/env/cameras/main_camera/Command',CameraCmd, tcp_nodelay=True, queue_size=10)
    if args.sim_sync:
        pub_limage = rospy.Publisher('/pss_limage/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
        pub_rimage = rospy.Publisher('/pss_rimage/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
        pub_pose_pan = rospy.Publisher('/pss_pose_pan',PoseStamped, tcp_nodelay=True, queue_size=10)
        pub_pose_drill = rospy.Publisher('/pss_pose_drill',PoseStamped, tcp_nodelay=True, queue_size=10)
        pub_pose_camhand = rospy.Publisher('/pss_pose_camhand',PoseStamped, tcp_nodelay=True, queue_size=10)
    if args.eval_tip_rpj:
        pub_eval_image = rospy.Publisher('/eval_drill/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
    if args.eval_segm:
        segm_sub = message_filters.Subscriber('/ambf/env/cameras/segmentation_camera/ImageData/compressed', CompressedImage) ##'/ambf/env/cameras/segmentation_camera/ImageData/compressed'
        pub_eval_segm = rospy.Publisher('/eval_segm/compressed',CompressedImage, tcp_nodelay=True, queue_size=10)
        ts = message_filters.ApproximateTimeSynchronizer([pose_camhand_sub, pose_drill_sub, pose_pan_sub, limage_sub, segm_sub], 50, 0.5)
        ts.registerCallback(callback)
    else:
        ts = message_filters.ApproximateTimeSynchronizer([pose_camhand_sub, pose_drill_sub, pose_pan_sub, limage_sub, rimage_sub], 50, 0.5)
        ts.registerCallback(callback)

    x_sub = rospy.Subscriber('/camera/xyz_offset', Float32MultiArray, cam_offset_cb, queue_size=1)

    rospy.spin()
    rospy.on_shutdown(my_shutdown_hook)

    
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--handeye", dest="X_path", help="path of handeye transformation X", default='hand_eye_X.npy', type=str)
    parser.add_argument("--eval_tip_rpj", dest='eval_tip_rpj', help='pulish images to evaluate the drill tip reprojection.', action='store_true')
    parser.add_argument("--eval_segm", dest='eval_segm', help='pulish images to evaluate the overlay of segmentation mask and the real scene.', action='store_true')
    parser.add_argument("--sim_sync", dest='sim_sync', help='sync the recorded images with the sim scene.', action='store_true')

    args = parser.parse_args()
    
    main()
    #<param name="gscam_config" value="decklinkvideosrc device-number=0 mode=1080i5994 connection=sdi ! deinterlace method = scalerbob ! videoconvert "/>
