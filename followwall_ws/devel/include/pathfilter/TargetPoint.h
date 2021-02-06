// Generated by gencpp from file pathfilter/TargetPoint.msg
// DO NOT EDIT!


#ifndef PATHFILTER_MESSAGE_TARGETPOINT_H
#define PATHFILTER_MESSAGE_TARGETPOINT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace pathfilter
{
template <class ContainerAllocator>
struct TargetPoint_
{
  typedef TargetPoint_<ContainerAllocator> Type;

  TargetPoint_()
    : targetPointx(0.0)
    , targetPointy(0.0)  {
    }
  TargetPoint_(const ContainerAllocator& _alloc)
    : targetPointx(0.0)
    , targetPointy(0.0)  {
  (void)_alloc;
    }



   typedef float _targetPointx_type;
  _targetPointx_type targetPointx;

   typedef float _targetPointy_type;
  _targetPointy_type targetPointy;





  typedef boost::shared_ptr< ::pathfilter::TargetPoint_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::pathfilter::TargetPoint_<ContainerAllocator> const> ConstPtr;

}; // struct TargetPoint_

typedef ::pathfilter::TargetPoint_<std::allocator<void> > TargetPoint;

typedef boost::shared_ptr< ::pathfilter::TargetPoint > TargetPointPtr;
typedef boost::shared_ptr< ::pathfilter::TargetPoint const> TargetPointConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::pathfilter::TargetPoint_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::pathfilter::TargetPoint_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace pathfilter

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/kinetic/share/nav_msgs/cmake/../msg'], 'pathfilter': ['/home/czp/followwall_ws/src/pathfilter/msg'], 'sensor_msgs': ['/opt/ros/kinetic/share/sensor_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::pathfilter::TargetPoint_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pathfilter::TargetPoint_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pathfilter::TargetPoint_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pathfilter::TargetPoint_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pathfilter::TargetPoint_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pathfilter::TargetPoint_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::pathfilter::TargetPoint_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8130f5abfd562a781ef67d6748766a3a";
  }

  static const char* value(const ::pathfilter::TargetPoint_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8130f5abfd562a78ULL;
  static const uint64_t static_value2 = 0x1ef67d6748766a3aULL;
};

template<class ContainerAllocator>
struct DataType< ::pathfilter::TargetPoint_<ContainerAllocator> >
{
  static const char* value()
  {
    return "pathfilter/TargetPoint";
  }

  static const char* value(const ::pathfilter::TargetPoint_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::pathfilter::TargetPoint_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 targetPointx\n\
float32 targetPointy\n\
";
  }

  static const char* value(const ::pathfilter::TargetPoint_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::pathfilter::TargetPoint_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.targetPointx);
      stream.next(m.targetPointy);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct TargetPoint_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::pathfilter::TargetPoint_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::pathfilter::TargetPoint_<ContainerAllocator>& v)
  {
    s << indent << "targetPointx: ";
    Printer<float>::stream(s, indent + "  ", v.targetPointx);
    s << indent << "targetPointy: ";
    Printer<float>::stream(s, indent + "  ", v.targetPointy);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PATHFILTER_MESSAGE_TARGETPOINT_H