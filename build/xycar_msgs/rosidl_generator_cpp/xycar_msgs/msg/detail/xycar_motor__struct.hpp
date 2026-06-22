// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_HPP_

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

#ifndef _WIN32
# define DEPRECATED__xycar_msgs__msg__XycarMotor __attribute__((deprecated))
#else
# define DEPRECATED__xycar_msgs__msg__XycarMotor __declspec(deprecated)
#endif

namespace xycar_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct XycarMotor_
{
  using Type = XycarMotor_<ContainerAllocator>;

  explicit XycarMotor_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->angle = 0.0f;
      this->speed = 0.0f;
    }
  }

  explicit XycarMotor_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->angle = 0.0f;
      this->speed = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _angle_type =
    float;
  _angle_type angle;
  using _speed_type =
    float;
  _speed_type speed;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__angle(
    const float & _arg)
  {
    this->angle = _arg;
    return *this;
  }
  Type & set__speed(
    const float & _arg)
  {
    this->speed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xycar_msgs::msg::XycarMotor_<ContainerAllocator> *;
  using ConstRawPtr =
    const xycar_msgs::msg::XycarMotor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xycar_msgs::msg::XycarMotor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xycar_msgs::msg::XycarMotor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xycar_msgs__msg__XycarMotor
    std::shared_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xycar_msgs__msg__XycarMotor
    std::shared_ptr<xycar_msgs::msg::XycarMotor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const XycarMotor_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->angle != other.angle) {
      return false;
    }
    if (this->speed != other.speed) {
      return false;
    }
    return true;
  }
  bool operator!=(const XycarMotor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct XycarMotor_

// alias to use template instance with default allocator
using XycarMotor =
  xycar_msgs::msg::XycarMotor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace xycar_msgs

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_HPP_
