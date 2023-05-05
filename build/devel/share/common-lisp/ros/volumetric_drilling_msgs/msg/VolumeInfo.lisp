; Auto-generated. Do not edit!


(cl:in-package volumetric_drilling_msgs-msg)


;//! \htmlinclude VolumeInfo.msg.html

(cl:defclass <VolumeInfo> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (dimensions
    :reader dimensions
    :initarg :dimensions
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (voxel_count
    :reader voxel_count
    :initarg :voxel_count
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass VolumeInfo (<VolumeInfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <VolumeInfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'VolumeInfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name volumetric_drilling_msgs-msg:<VolumeInfo> is deprecated: use volumetric_drilling_msgs-msg:VolumeInfo instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <VolumeInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:header-val is deprecated.  Use volumetric_drilling_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <VolumeInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:pose-val is deprecated.  Use volumetric_drilling_msgs-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'dimensions-val :lambda-list '(m))
(cl:defmethod dimensions-val ((m <VolumeInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:dimensions-val is deprecated.  Use volumetric_drilling_msgs-msg:dimensions instead.")
  (dimensions m))

(cl:ensure-generic-function 'voxel_count-val :lambda-list '(m))
(cl:defmethod voxel_count-val ((m <VolumeInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:voxel_count-val is deprecated.  Use volumetric_drilling_msgs-msg:voxel_count instead.")
  (voxel_count m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <VolumeInfo>) ostream)
  "Serializes a message object of type '<VolumeInfo>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'dimensions))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'dimensions))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'voxel_count))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'voxel_count))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <VolumeInfo>) istream)
  "Deserializes a message object of type '<VolumeInfo>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'dimensions) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'dimensions)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'voxel_count) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'voxel_count)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<VolumeInfo>)))
  "Returns string type for a message object of type '<VolumeInfo>"
  "volumetric_drilling_msgs/VolumeInfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'VolumeInfo)))
  "Returns string type for a message object of type 'VolumeInfo"
  "volumetric_drilling_msgs/VolumeInfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<VolumeInfo>)))
  "Returns md5sum for a message object of type '<VolumeInfo>"
  "eca5e1d3f35a79d6d1cc4d0b1037724c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'VolumeInfo)))
  "Returns md5sum for a message object of type 'VolumeInfo"
  "eca5e1d3f35a79d6d1cc4d0b1037724c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<VolumeInfo>)))
  "Returns full string definition for message of type '<VolumeInfo>"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Pose pose~%float32[] dimensions~%int32[] voxel_count~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'VolumeInfo)))
  "Returns full string definition for message of type 'VolumeInfo"
  (cl:format cl:nil "std_msgs/Header header~%geometry_msgs/Pose pose~%float32[] dimensions~%int32[] voxel_count~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <VolumeInfo>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'dimensions) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'voxel_count) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <VolumeInfo>))
  "Converts a ROS message object to a list"
  (cl:list 'VolumeInfo
    (cl:cons ':header (header msg))
    (cl:cons ':pose (pose msg))
    (cl:cons ':dimensions (dimensions msg))
    (cl:cons ':voxel_count (voxel_count msg))
))
