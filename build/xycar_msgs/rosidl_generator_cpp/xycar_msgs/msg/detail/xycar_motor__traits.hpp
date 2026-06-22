// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__TRAITS_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xycar_msgs/msg/detail/xycar_motor__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace xycar_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const XycarMotor & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: angle
  {
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << ", ";
  }

  // member: speed
  {
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const XycarMotor & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << "\n";
  }

  // member: speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const XycarMotor & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace xycar_msgs

namespace rosidl_generator_traits
{

[[deprecated("use xycar_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const xycar_msgs::msg::XycarMotor & msg,
  std::ostream & out, size_t indentation = 0)
{
  xycar_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xycar_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const xycar_msgs::msg::XycarMotor & msg)
{
  return xycar_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<xycar_msgs::msg::XycarMotor>()
{
  return "xycar_msgs::msg::XycarMotor";
}

template<>
inline const char * name<xycar_msgs::msg::XycarMotor>()
{
  return "xycar_msgs/msg/XycarMotor";
}

template<>
struct has_fixed_size<xycar_msgs::msg::XycarMotor>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<xycar_msgs::msg::XycarMotor>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<xycar_msgs::msg::XycarMotor>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__TRAITS_HPP_
