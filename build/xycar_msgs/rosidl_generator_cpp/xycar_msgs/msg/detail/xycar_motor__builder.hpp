// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__BUILDER_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xycar_msgs/msg/detail/xycar_motor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xycar_msgs
{

namespace msg
{

namespace builder
{

class Init_XycarMotor_speed
{
public:
  explicit Init_XycarMotor_speed(::xycar_msgs::msg::XycarMotor & msg)
  : msg_(msg)
  {}
  ::xycar_msgs::msg::XycarMotor speed(::xycar_msgs::msg::XycarMotor::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xycar_msgs::msg::XycarMotor msg_;
};

class Init_XycarMotor_angle
{
public:
  explicit Init_XycarMotor_angle(::xycar_msgs::msg::XycarMotor & msg)
  : msg_(msg)
  {}
  Init_XycarMotor_speed angle(::xycar_msgs::msg::XycarMotor::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return Init_XycarMotor_speed(msg_);
  }

private:
  ::xycar_msgs::msg::XycarMotor msg_;
};

class Init_XycarMotor_header
{
public:
  Init_XycarMotor_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_XycarMotor_angle header(::xycar_msgs::msg::XycarMotor::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_XycarMotor_angle(msg_);
  }

private:
  ::xycar_msgs::msg::XycarMotor msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::xycar_msgs::msg::XycarMotor>()
{
  return xycar_msgs::msg::builder::Init_XycarMotor_header();
}

}  // namespace xycar_msgs

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__BUILDER_HPP_
