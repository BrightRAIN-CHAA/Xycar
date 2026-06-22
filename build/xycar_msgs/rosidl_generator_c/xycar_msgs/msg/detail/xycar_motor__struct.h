// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_H_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/XycarMotor in the package xycar_msgs.
typedef struct xycar_msgs__msg__XycarMotor
{
  std_msgs__msg__Header header;
  float angle;
  float speed;
} xycar_msgs__msg__XycarMotor;

// Struct for a sequence of xycar_msgs__msg__XycarMotor.
typedef struct xycar_msgs__msg__XycarMotor__Sequence
{
  xycar_msgs__msg__XycarMotor * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xycar_msgs__msg__XycarMotor__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__STRUCT_H_
