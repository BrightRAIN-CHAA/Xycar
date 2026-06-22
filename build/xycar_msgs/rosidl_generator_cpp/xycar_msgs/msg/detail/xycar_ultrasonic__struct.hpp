// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'ranges'
#include "sensor_msgs/msg/detail/range__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__xycar_msgs__msg__XycarUltrasonic __attribute__((deprecated))
#else
# define DEPRECATED__xycar_msgs__msg__XycarUltrasonic __declspec(deprecated)
#endif

namespace xycar_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct XycarUltrasonic_
{
  using Type = XycarUltrasonic_<ContainerAllocator>;

  explicit XycarUltrasonic_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit XycarUltrasonic_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _ranges_type =
    std::vector<sensor_msgs::msg::Range_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<sensor_msgs::msg::Range_<ContainerAllocator>>>;
  _ranges_type ranges;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__ranges(
    const std::vector<sensor_msgs::msg::Range_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<sensor_msgs::msg::Range_<ContainerAllocator>>> & _arg)
  {
    this->ranges = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> *;
  using ConstRawPtr =
    const xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xycar_msgs__msg__XycarUltrasonic
    std::shared_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xycar_msgs__msg__XycarUltrasonic
    std::shared_ptr<xycar_msgs::msg::XycarUltrasonic_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const XycarUltrasonic_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->ranges != other.ranges) {
      return false;
    }
    return true;
  }
  bool operator!=(const XycarUltrasonic_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct XycarUltrasonic_

// alias to use template instance with default allocator
using XycarUltrasonic =
  xycar_msgs::msg::XycarUltrasonic_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace xycar_msgs

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_HPP_
