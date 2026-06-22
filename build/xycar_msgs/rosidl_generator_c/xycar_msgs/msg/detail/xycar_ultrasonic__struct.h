// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_H_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_H_

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
// Member 'ranges'
#include "sensor_msgs/msg/detail/range__struct.h"

/// Struct defined in msg/XycarUltrasonic in the package xycar_msgs.
typedef struct xycar_msgs__msg__XycarUltrasonic
{
  std_msgs__msg__Header header;
  sensor_msgs__msg__Range__Sequence ranges;
} xycar_msgs__msg__XycarUltrasonic;

// Struct for a sequence of xycar_msgs__msg__XycarUltrasonic.
typedef struct xycar_msgs__msg__XycarUltrasonic__Sequence
{
  xycar_msgs__msg__XycarUltrasonic * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xycar_msgs__msg__XycarUltrasonic__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_ULTRASONIC__STRUCT_H_
