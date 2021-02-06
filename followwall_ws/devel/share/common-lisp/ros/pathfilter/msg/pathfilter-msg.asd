
(cl:in-package :asdf)

(defsystem "pathfilter-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "TargetPoint" :depends-on ("_package_TargetPoint"))
    (:file "_package_TargetPoint" :depends-on ("_package"))
    (:file "Traj" :depends-on ("_package_Traj"))
    (:file "_package_Traj" :depends-on ("_package"))
  ))