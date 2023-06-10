import rospy
from geometry_msgs.msg import PoseStamped
import numpy as np

def publish_poses(all_poses):
    rospy.init_node('pose_publisher', anonymous=True)
    
    # Create PoseStamped publishers
    num_poses = all_poses.shape[0]
    num_publishers = all_poses.shape[1]  # Number of poses
    publishers = []
    obj = ['drill', 'phacon']
    for i in range(num_publishers):
        topic_name = '/pose_publisher/pose_{}'.format(obj[i])  # Topic name for each publisher
        publishers.append(rospy.Publisher(topic_name, PoseStamped, queue_size=10))

    rate = rospy.Rate(30)  # Publishing rate in Hz
    while not rospy.is_shutdown():
        for i in range(num_poses):
            poses = all_poses[i]
            for j in range(num_publishers):
                pose = poses[j]
                
                # Create a PoseStamped message
                pose_stamped = PoseStamped()
                pose_stamped.header.stamp = rospy.Time.now()
                pose_stamped.header.frame_id = 'map'  # Frame ID
                pose_stamped.pose.position.x = pose[0]  # X coordinate
                pose_stamped.pose.position.y = pose[1]  # Y coordinate
                pose_stamped.pose.position.z = pose[2]  # Z coordinate
                pose_stamped.pose.orientation.x = pose[3]
                pose_stamped.pose.orientation.y = pose[4]
                pose_stamped.pose.orientation.z = pose[5]
                pose_stamped.pose.orientation.w = pose[6]
                # Publish the PoseStamped message
                publishers[j].publish(pose_stamped)

            rate.sleep()
    
if __name__ == '__main__':
    # Example numpy array representing poses (3D coordinates)
    t = np.zeros([1000,2,7])
    t[:,:,-1] = 1
    t[:,0,0] = np.linspace(0,1,1000)
    try:
        publish_poses(t)
    except rospy.ROSInterruptException:
        pass
