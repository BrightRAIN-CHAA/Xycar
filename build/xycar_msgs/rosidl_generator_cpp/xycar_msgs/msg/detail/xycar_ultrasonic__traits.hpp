// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__TRAITS_HPP_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xycar_msgs/msg/detail/xycar_ultrasonic__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'ranges'
#include "sensor_msgs/msg/detail/range__traits.hpp"

namespace xycar_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const XycarUltrasonic & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: ranges
  {
    if (msg.ranges.size() == 0) {
      out << "ranges: []";
    } else {
      out << "ranges: [";
      size_t pending_items = msg.ranges.size();
      for (auto item : msg.ranges) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const XycarUltrasonic & msg,
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

  // member: ranges
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.ranges.size() == 0) {
      out << "ranges: []\n";
    } else {
      out << "ranges:\n";
      for (auto item : msg.ranges) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const XycarUltrasonic & msg, bool use_flow_style = false)
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
  const xycar_msgs::msg::XycarUltrasonic & msg,
  std::ostream & out, size_t indentation = 0)
{
  xycar_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xycar_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const xycar_msgs::msg::XycarUltrasonic & msg)
{
  return xycar_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<xycar_msgs::msg::XycarUltrasonic>()
{
  return "xycar_msgs::msg::XycarUltrasonic";
}

template<>
inline const char * name<xycar_msgs::msg::XycarUltrasonic>()
{
  return "xycar_msgs/msg/XycarUltrasonic";
}

template<>
struct has_fixed_size<xycar_msgs::msg::XycarUltrasonic>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<xycar_msgs::msg::XycarUltrasonic>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<xycar_msgs::msg::XycarUltrasonic>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__TRAITS_HPP_
