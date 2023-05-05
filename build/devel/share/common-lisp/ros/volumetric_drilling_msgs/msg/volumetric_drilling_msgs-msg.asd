
(cl:in-package :asdf)

(defsystem "volumetric_drilling_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "DrillSize" :depends-on ("_package_DrillSize"))
    (:file "_package_DrillSize" :depends-on ("_package"))
    (:file "Index" :depends-on ("_package_Index"))
    (:file "_package_Index" :depends-on ("_package"))
    (:file "VolumeInfo" :depends-on ("_package_VolumeInfo"))
    (:file "_package_VolumeInfo" :depends-on ("_package"))
    (:file "Voxels" :depends-on ("_package_Voxels"))
    (:file "_package_Voxels" :depends-on ("_package"))
  ))