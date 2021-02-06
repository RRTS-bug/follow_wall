;; Auto-generated. Do not edit!


(when (boundp 'pathfilter::TargetPoint)
  (if (not (find-package "PATHFILTER"))
    (make-package "PATHFILTER"))
  (shadow 'TargetPoint (find-package "PATHFILTER")))
(unless (find-package "PATHFILTER::TARGETPOINT")
  (make-package "PATHFILTER::TARGETPOINT"))

(in-package "ROS")
;;//! \htmlinclude TargetPoint.msg.html


(defclass pathfilter::TargetPoint
  :super ros::object
  :slots (_targetPointx _targetPointy ))

(defmethod pathfilter::TargetPoint
  (:init
   (&key
    ((:targetPointx __targetPointx) 0.0)
    ((:targetPointy __targetPointy) 0.0)
    )
   (send-super :init)
   (setq _targetPointx (float __targetPointx))
   (setq _targetPointy (float __targetPointy))
   self)
  (:targetPointx
   (&optional __targetPointx)
   (if __targetPointx (setq _targetPointx __targetPointx)) _targetPointx)
  (:targetPointy
   (&optional __targetPointy)
   (if __targetPointy (setq _targetPointy __targetPointy)) _targetPointy)
  (:serialization-length
   ()
   (+
    ;; float32 _targetPointx
    4
    ;; float32 _targetPointy
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _targetPointx
       (sys::poke _targetPointx (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _targetPointy
       (sys::poke _targetPointy (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _targetPointx
     (setq _targetPointx (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _targetPointy
     (setq _targetPointy (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get pathfilter::TargetPoint :md5sum-) "8130f5abfd562a781ef67d6748766a3a")
(setf (get pathfilter::TargetPoint :datatype-) "pathfilter/TargetPoint")
(setf (get pathfilter::TargetPoint :definition-)
      "float32 targetPointx
float32 targetPointy
")



(provide :pathfilter/TargetPoint "8130f5abfd562a781ef67d6748766a3a")


