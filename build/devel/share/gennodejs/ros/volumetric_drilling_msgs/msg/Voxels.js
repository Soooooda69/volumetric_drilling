// Auto-generated. Do not edit!

// (in-package volumetric_drilling_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Index = require('./Index.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class Voxels {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.indices = null;
      this.colors = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('indices')) {
        this.indices = initObj.indices
      }
      else {
        this.indices = [];
      }
      if (initObj.hasOwnProperty('colors')) {
        this.colors = initObj.colors
      }
      else {
        this.colors = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Voxels
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [indices]
    // Serialize the length for message field [indices]
    bufferOffset = _serializer.uint32(obj.indices.length, buffer, bufferOffset);
    obj.indices.forEach((val) => {
      bufferOffset = Index.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [colors]
    // Serialize the length for message field [colors]
    bufferOffset = _serializer.uint32(obj.colors.length, buffer, bufferOffset);
    obj.colors.forEach((val) => {
      bufferOffset = std_msgs.msg.ColorRGBA.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Voxels
    let len;
    let data = new Voxels(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [indices]
    // Deserialize array length for message field [indices]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.indices = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.indices[i] = Index.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [colors]
    // Deserialize array length for message field [colors]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.colors = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.colors[i] = std_msgs.msg.ColorRGBA.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 24 * object.indices.length;
    length += 16 * object.colors.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'volumetric_drilling_msgs/Voxels';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7cd932ee96e95d914af050c7da8c2ecf';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Voxels(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.indices !== undefined) {
      resolved.indices = new Array(msg.indices.length);
      for (let i = 0; i < resolved.indices.length; ++i) {
        resolved.indices[i] = Index.Resolve(msg.indices[i]);
      }
    }
    else {
      resolved.indices = []
    }

    if (msg.colors !== undefined) {
      resolved.colors = new Array(msg.colors.length);
      for (let i = 0; i < resolved.colors.length; ++i) {
        resolved.colors[i] = std_msgs.msg.ColorRGBA.Resolve(msg.colors[i]);
      }
    }
    else {
      resolved.colors = []
    }

    return resolved;
    }
};

module.exports = Voxels;
