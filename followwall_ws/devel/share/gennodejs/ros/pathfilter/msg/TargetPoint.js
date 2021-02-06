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

class TargetPoint {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.targetPointx = null;
      this.targetPointy = null;
    }
    else {
      if (initObj.hasOwnProperty('targetPointx')) {
        this.targetPointx = initObj.targetPointx
      }
      else {
        this.targetPointx = 0.0;
      }
      if (initObj.hasOwnProperty('targetPointy')) {
        this.targetPointy = initObj.targetPointy
      }
      else {
        this.targetPointy = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TargetPoint
    // Serialize message field [targetPointx]
    bufferOffset = _serializer.float32(obj.targetPointx, buffer, bufferOffset);
    // Serialize message field [targetPointy]
    bufferOffset = _serializer.float32(obj.targetPointy, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TargetPoint
    let len;
    let data = new TargetPoint(null);
    // Deserialize message field [targetPointx]
    data.targetPointx = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [targetPointy]
    data.targetPointy = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'pathfilter/TargetPoint';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8130f5abfd562a781ef67d6748766a3a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 targetPointx
    float32 targetPointy
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TargetPoint(null);
    if (msg.targetPointx !== undefined) {
      resolved.targetPointx = msg.targetPointx;
    }
    else {
      resolved.targetPointx = 0.0
    }

    if (msg.targetPointy !== undefined) {
      resolved.targetPointy = msg.targetPointy;
    }
    else {
      resolved.targetPointy = 0.0
    }

    return resolved;
    }
};

module.exports = TargetPoint;
