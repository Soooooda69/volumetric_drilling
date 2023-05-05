; Auto-generated. Do not edit!


(cl:in-package volumetric_drilling_msgs-msg)


;//! \htmlinclude Voxels.msg.html

(cl:defclass <Voxels> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (indices
    :reader indices
    :initarg :indices
    :type (cl:vector volumetric_drilling_msgs-msg:Index)
   :initform (cl:make-array 0 :element-type 'volumetric_drilling_msgs-msg:Index :initial-element (cl:make-instance 'volumetric_drilling_msgs-msg:Index)))
   (colors
    :reader colors
    :initarg :colors
    :type (cl:vector std_msgs-msg:ColorRGBA)
   :initform (cl:make-array 0 :element-type 'std_msgs-msg:ColorRGBA :initial-element (cl:make-instance 'std_msgs-msg:ColorRGBA))))
)

(cl:defclass Voxels (<Voxels>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Voxels>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Voxels)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name volumetric_drilling_msgs-msg:<Voxels> is deprecated: use volumetric_drilling_msgs-msg:Voxels instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <Voxels>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:header-val is deprecated.  Use volumetric_drilling_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'indices-val :lambda-list '(m))
(cl:defmethod indices-val ((m <Voxels>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:indices-val is deprecated.  Use volumetric_drilling_msgs-msg:indices instead.")
  (indices m))

(cl:ensure-generic-function 'colors-val :lambda-list '(m))
(cl:defmethod colors-val ((m <Voxels>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader volumetric_drilling_msgs-msg:colors-val is deprecated.  Use volumetric_drilling_msgs-msg:colors instead.")
  (colors m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Voxels>) ostream)
  "Serializes a message object of type '<Voxels>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'indices))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'indices))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'colors))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'colors))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Voxels>) istream)
  "Deserializes a message object of type '<Voxels>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'indices) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'indices)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'volumetric_drilling_msgs-msg:Index))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'colors) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'colors)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'std_msgs-msg:ColorRGBA))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Voxels>)))
  "Returns string type for a message object of type '<Voxels>"
  "volumetric_drilling_msgs/Voxels")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Voxels)))
  "Returns string type for a message object of type 'Voxels"
  "volumetric_drilling_msgs/Voxels")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Voxels>)))
  "Returns md5sum for a message object of type '<Voxels>"
  "7cd932ee96e95d914af050c7da8c2ecf")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Voxels)))
  "Returns md5sum for a message object of type 'Voxels"
  "7cd932ee96e95d914af050c7da8c2ecf")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Voxels>)))
  "Returns full string definition for message of type '<Voxels>"
  (cl:format cl:nil "std_msgs/Header header~%Index[] indices~%std_msgs/ColorRGBA[] colors~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: volumetric_drilling_msgs/Index~%int64 x~%int64 y~%int64 z~%~%================================================================================~%MSG: std_msgs/ColorRGBA~%float32 r~%float32 g~%float32 b~%float32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Voxels)))
  "Returns full string definition for message of type 'Voxels"
  (cl:format cl:nil "std_msgs/Header header~%Index[] indices~%std_msgs/ColorRGBA[] colors~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: volumetric_drilling_msgs/Index~%int64 x~%int64 y~%int64 z~%~%================================================================================~%MSG: std_msgs/ColorRGBA~%float32 r~%float32 g~%float32 b~%float32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Voxels>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'indices) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'colors) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Voxels>))
  "Converts a ROS message object to a list"
  (cl:list 'Voxels
    (cl:cons ':header (header msg))
    (cl:cons ':indices (indices msg))
    (cl:cons ':colors (colors msg))
))
