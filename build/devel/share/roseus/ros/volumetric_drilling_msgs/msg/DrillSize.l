;; Auto-generated. Do not edit!


(when (boundp 'volumetric_drilling_msgs::DrillSize)
  (if (not (find-package "VOLUMETRIC_DRILLING_MSGS"))
    (make-package "VOLUMETRIC_DRILLING_MSGS"))
  (shadow 'DrillSize (find-package "VOLUMETRIC_DRILLING_MSGS")))
(unless (find-package "VOLUMETRIC_DRILLING_MSGS::DRILLSIZE")
  (make-package "VOLUMETRIC_DRILLING_MSGS::DRILLSIZE"))

(in-package "ROS")
;;//! \htmlinclude DrillSize.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass volumetric_drilling_msgs::DrillSize
  :super ros::object
  :slots (_header _size ))

(defmethod volumetric_drilling_msgs::DrillSize
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:size __size) (instance std_msgs::UInt8 :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _size __size)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:size
   (&rest __size)
   (if (keywordp (car __size))
       (send* _size __size)
     (progn
       (if __size (setq _size (car __size)))
       _size)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; std_msgs/UInt8 _size
    (send _size :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; std_msgs/UInt8 _size
       (send _size :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; std_msgs/UInt8 _size
     (send _size :deserialize buf ptr-) (incf ptr- (send _size :serialization-length))
   ;;
   self)
  )

(setf (get volumetric_drilling_msgs::DrillSize :md5sum-) "d9d4da25c106b8208dccc4d469ec477b")
(setf (get volumetric_drilling_msgs::DrillSize :datatype-) "volumetric_drilling_msgs/DrillSize")
(setf (get volumetric_drilling_msgs::DrillSize :definition-)
      "std_msgs/Header header
std_msgs/UInt8 size

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
MSG: std_msgs/UInt8
uint8 data

")



(provide :volumetric_drilling_msgs/DrillSize "d9d4da25c106b8208dccc4d469ec477b")


