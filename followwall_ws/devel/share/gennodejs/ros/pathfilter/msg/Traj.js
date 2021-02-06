// Auto-generated. Do not edit!

// (in-package pathfilter.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Traj {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.trajectoryX = null;
      this.trajectoryY = null;
    }
    else {
      if (initObj.hasOwnProperty('trajectoryX')) {
        this.trajectoryX = initObj.trajectoryX
      }
      else {
        this.trajectoryX = [];
      }
      if (initObj.hasOwnProperty('trajectoryY')) {
        this.trajectoryY = initObj.trajectoryY
      }
      else {
        this.trajectoryY = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Traj
    // Serialize message field [trajectoryX]
    bufferOffset = _arraySerializer.float32(obj.trajectoryX, buffer, bufferOffset, null);
    // Serialize message field [trajectoryY]
    bufferOffset = _arraySerializer.float32(obj.trajectoryY, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Traj
    let len;
    let data = new Traj(null);
    // Deserialize message field [trajectoryX]
    data.trajectoryX = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [trajectoryY]
    data.trajectoryY = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.trajectoryX.length;
    length += 4 * object.trajectoryY.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'pathfilter/Traj';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2343a9eebc0c84e51eef389e14d15ade';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32[] trajectoryX
    float32[] trajectoryY
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Traj(null);
    if (msg.trajectoryX !== undefined) {
      resolved.trajectoryX = msg.trajectoryX;
    }
    else {
      resolved.trajectoryX = []
    }

    if (msg.trajectoryY !== undefined) {
      resolved.trajectoryY = msg.trajectoryY;
    }
    else {
      resolved.trajectoryY = []
    }

    return resolved;
    }
};

module.exports = Traj;
