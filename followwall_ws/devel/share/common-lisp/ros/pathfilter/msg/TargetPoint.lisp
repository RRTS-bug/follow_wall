; Auto-generated. Do not edit!


(cl:in-package pathfilter-msg)


;//! \htmlinclude TargetPoint.msg.html

(cl:defclass <TargetPoint> (roslisp-msg-protocol:ros-message)
  ((targetPointx
    :reader targetPointx
    :initarg :targetPointx
    :type cl:float
    :initform 0.0)
   (targetPointy
    :reader targetPointy
    :initarg :targetPointy
    :type cl:float
    :initform 0.0))
)

(cl:defclass TargetPoint (<TargetPoint>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TargetPoint>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TargetPoint)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pathfilter-msg:<TargetPoint> is deprecated: use pathfilter-msg:TargetPoint instead.")))

(cl:ensure-generic-function 'targetPointx-val :lambda-list '(m))
(cl:defmethod targetPointx-val ((m <TargetPoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pathfilter-msg:targetPointx-val is deprecated.  Use pathfilter-msg:targetPointx instead.")
  (targetPointx m))

(cl:ensure-generic-function 'targetPointy-val :lambda-list '(m))
(cl:defmethod targetPointy-val ((m <TargetPoint>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pathfilter-msg:targetPointy-val is deprecated.  Use pathfilter-msg:targetPointy instead.")
  (targetPointy m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TargetPoint>) ostream)
  "Serializes a message object of type '<TargetPoint>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'targetPointx))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'targetPointy))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TargetPoint>) istream)
  "Deserializes a message object of type '<TargetPoint>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'targetPointx) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'targetPointy) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TargetPoint>)))
  "Returns string type for a message object of type '<TargetPoint>"
  "pathfilter/TargetPoint")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TargetPoint)))
  "Returns string type for a message object of type 'TargetPoint"
  "pathfilter/TargetPoint")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TargetPoint>)))
  "Returns md5sum for a message object of type '<TargetPoint>"
  "8130f5abfd562a781ef67d6748766a3a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TargetPoint)))
  "Returns md5sum for a message object of type 'TargetPoint"
  "8130f5abfd562a781ef67d6748766a3a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TargetPoint>)))
  "Returns full string definition for message of type '<TargetPoint>"
  (cl:format cl:nil "float32 targetPointx~%float32 targetPointy~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TargetPoint)))
  "Returns full string definition for message of type 'TargetPoint"
  (cl:format cl:nil "float32 targetPointx~%float32 targetPointy~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TargetPoint>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TargetPoint>))
  "Converts a ROS message object to a list"
  (cl:list 'TargetPoint
    (cl:cons ':targetPointx (targetPointx msg))
    (cl:cons ':targetPointy (targetPointy msg))
))
