// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__BUILDER_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xycar_msgs/msg/detail/xycar_ultrasonic__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xycar_msgs
{

namespace msg
{

namespace builder
{

class Init_XycarUltrasonic_ranges
{
public:
  explicit Init_XycarUltrasonic_ranges(::xycar_msgs::msg::XycarUltrasonic & msg)
  : msg_(msg)
  {}
  ::xycar_msgs::msg::XycarUltrasonic ranges(::xycar_msgs::msg::XycarUltrasonic::_ranges_type arg)
  {
    msg_.ranges = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xycar_msgs::msg::XycarUltrasonic msg_;
};

class Init_XycarUltrasonic_header
{
public:
  Init_XycarUltrasonic_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_XycarUltrasonic_ranges header(::xycar_msgs::msg::XycarUltrasonic::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_XycarUltrasonic_ranges(msg_);
  }

private:
  ::xycar_msgs::msg::XycarUltrasonic msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::xycar_msgs::msg::XycarUltrasonic>()
{
  return xycar_msgs::msg::builder::Init_XycarUltrasonic_header();
}

}  // namespace xycar_msgs

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__BUILDER_HPP_
