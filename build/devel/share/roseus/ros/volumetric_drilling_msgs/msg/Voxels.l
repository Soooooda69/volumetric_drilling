;; Auto-generated. Do not edit!


(when (boundp 'volumetric_drilling_msgs::Voxels)
  (if (not (find-package "VOLUMETRIC_DRILLING_MSGS"))
    (make-package "VOLUMETRIC_DRILLING_MSGS"))
  (shadow 'Voxels (find-package "VOLUMETRIC_DRILLING_MSGS")))
(unless (find-package "VOLUMETRIC_DRILLING_MSGS::VOXELS")
  (make-package "VOLUMETRIC_DRILLING_MSGS::VOXELS"))

(in-package "ROS")
;;//! \htmlinclude Voxels.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass volumetric_drilling_msgs::Voxels
  :super ros::object
  :slots (_header _indices _colors ))

(defmethod volumetric_drilling_msgs::Voxels
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:indices __indices) ())
    ((:colors __colors) ())
    )
   (send-super :init)
   (setq _header __header)
   (setq _indices __indices)
   (setq _colors __colors)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:indices
   (&rest __indices)
   (if (keywordp (car __indices))
       (send* _indices __indices)
     (progn
       (if __indices (setq _indices (car __indices)))
       _indices)))
  (:colors
   (&rest __colors)
   (if (keywordp (car __colors))
       (send* _colors __colors)
     (progn
       (if __colors (setq _colors (car __colors)))
       _colors)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; volumetric_drilling_msgs/Index[] _indices
    (apply #'+ (send-all _indices :serialization-length)) 4
    ;; std_msgs/ColorRGBA[] _colors
    (apply #'+ (send-all _colors :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; volumetric_drilling_msgs/Index[] _indices
     (write-long (length _indices) s)
     (dolist (elem _indices)
       (send elem :serialize s)
       )
     ;; std_msgs/ColorRGBA[] _colors
     (write-long (length _colors) s)
     (dolist (elem _colors)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; volumetric_drilling_msgs/Index[] _indices
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _indices (let (r) (dotimes (i n) (push (instance volumetric_drilling_msgs::Index :init) r)) r))
     (dolist (elem- _indices)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; std_msgs/ColorRGBA[] _colors
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _colors (let (r) (dotimes (i n) (push (instance std_msgs::ColorRGBA :init) r)) r))
     (dolist (elem- _colors)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get volumetric_drilling_msgs::Voxels :md5sum-) "7cd932ee96e95d914af050c7da8c2ecf")
(setf (get volumetric_drilling_msgs::Voxels :datatype-) "volumetric_drilling_msgs/Voxels")
(setf (get volumetric_drilling_msgs::Voxels :definition-)
      "std_msgs/Header header
Index[] indices
std_msgs/ColorRGBA[] colors

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
MSG: volumetric_drilling_msgs/Index
int64 x
int64 y
int64 z

================================================================================
MSG: std_msgs/ColorRGBA
float32 r
float32 g
float32 b
float32 a

")



(provide :volumetric_drilling_msgs/Voxels "7cd932ee96e95d914af050c7da8c2ecf")


