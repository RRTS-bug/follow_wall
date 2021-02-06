; Auto-generated. Do not edit!


(cl:in-package pathfilter-msg)


;//! \htmlinclude Traj.msg.html

(cl:defclass <Traj> (roslisp-msg-protocol:ros-message)
  ((trajectoryX
    :reader trajectoryX
    :initarg :trajectoryX
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (trajectoryY
    :reader trajectoryY
    :initarg :trajectoryY
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass Traj (<Traj>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Traj>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Traj)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pathfilter-msg:<Traj> is deprecated: use pathfilter-msg:Traj instead.")))

(cl:ensure-generic-function 'trajectoryX-val :lambda-list '(m))
(cl:defmethod trajectoryX-val ((m <Traj>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pathfilter-msg:trajectoryX-val is deprecated.  Use pathfilter-msg:trajectoryX instead.")
  (trajectoryX m))

(cl:ensure-generic-function 'trajectoryY-val :lambda-list '(m))
(cl:defmethod trajectoryY-val ((m <Traj>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pathfilter-msg:trajectoryY-val is deprecated.  Use pathfilter-msg:trajectoryY instead.")
  (trajectoryY m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Traj>) ostream)
  "Serializes a message object of type '<Traj>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'trajectoryX))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'trajectoryX))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'trajectoryY))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'trajectoryY))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Traj>) istream)
  "Deserializes a message object of type '<Traj>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'trajectoryX) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'trajectoryX)))
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
  (cl:setf (cl:slot-value msg 'trajectoryY) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'trajectoryY)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Traj>)))
  "Returns string type for a message object of type '<Traj>"
  "pathfilter/Traj")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Traj)))
  "Returns string type for a message object of type 'Traj"
  "pathfilter/Traj")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Traj>)))
  "Returns md5sum for a message object of type '<Traj>"
  "2343a9eebc0c84e51eef389e14d15ade")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Traj)))
  "Returns md5sum for a message object of type 'Traj"
  "2343a9eebc0c84e51eef389e14d15ade")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Traj>)))
  "Returns full string definition for message of type '<Traj>"
  (cl:format cl:nil "float32[] trajectoryX~%float32[] trajectoryY~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Traj)))
  "Returns full string definition for message of type 'Traj"
  (cl:format cl:nil "float32[] trajectoryX~%float32[] trajectoryY~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Traj>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'trajectoryX) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'trajectoryY) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Traj>))
  "Converts a ROS message object to a list"
  (cl:list 'Traj
    (cl:cons ':trajectoryX (trajectoryX msg))
    (cl:cons ':trajectoryY (trajectoryY msg))
))
