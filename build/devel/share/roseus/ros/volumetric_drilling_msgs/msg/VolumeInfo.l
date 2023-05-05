;; Auto-generated. Do not edit!


(when (boundp 'volumetric_drilling_msgs::VolumeInfo)
  (if (not (find-package "VOLUMETRIC_DRILLING_MSGS"))
    (make-package "VOLUMETRIC_DRILLING_MSGS"))
  (shadow 'VolumeInfo (find-package "VOLUMETRIC_DRILLING_MSGS")))
(unless (find-package "VOLUMETRIC_DRILLING_MSGS::VOLUMEINFO")
  (make-package "VOLUMETRIC_DRILLING_MSGS::VOLUMEINFO"))

(in-package "ROS")
;;//! \htmlinclude VolumeInfo.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass volumetric_drilling_msgs::VolumeInfo
  :super ros::object
  :slots (_header _pose _dimensions _voxel_count ))

(defmethod volumetric_drilling_msgs::VolumeInfo
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    ((:dimensions __dimensions) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:voxel_count __voxel_count) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _header __header)
   (setq _pose __pose)
   (setq _dimensions __dimensions)
   (setq _voxel_count __voxel_count)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:dimensions
   (&optional __dimensions)
   (if __dimensions (setq _dimensions __dimensions)) _dimensions)
  (:voxel_count
   (&optional __voxel_count)
   (if __voxel_count (setq _voxel_count __voxel_count)) _voxel_count)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ;; float32[] _dimensions
    (* 4    (length _dimensions)) 4
    ;; int32[] _voxel_count
    (* 4    (length _voxel_count)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;; float32[] _dimensions
     (write-long (length _dimensions) s)
     (dotimes (i (length _dimensions))
       (sys::poke (elt _dimensions i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; int32[] _voxel_count
     (write-long (length _voxel_count) s)
     (dotimes (i (length _voxel_count))
       (write-long (elt _voxel_count i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float32[] _dimensions
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _dimensions (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _dimensions i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; int32[] _voxel_count
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _voxel_count (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _voxel_count i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get volumetric_drilling_msgs::VolumeInfo :md5sum-) "eca5e1d3f35a79d6d1cc4d0b1037724c")
(setf (get volumetric_drilling_msgs::VolumeInfo :datatype-) "volumetric_drilling_msgs/VolumeInfo")
(setf (get volumetric_drilling_msgs::VolumeInfo :definition-)
      "std_msgs/Header header
geometry_msgs/Pose pose
float32[] dimensions
int32[] voxel_count

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :volumetric_drilling_msgs/VolumeInfo "eca5e1d3f35a79d6d1cc4d0b1037724c")


