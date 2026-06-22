// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "xycar_msgs/msg/detail/xycar_ultrasonic__rosidl_typesupport_introspection_c.h"
#include "xycar_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "xycar_msgs/msg/detail/xycar_ultrasonic__functions.h"
#include "xycar_msgs/msg/detail/xycar_ultrasonic__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `ranges`
#include "sensor_msgs/msg/range.h"
// Member `ranges`
#include "sensor_msgs/msg/detail/range__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  xycar_msgs__msg__XycarUltrasonic__init(message_memory);
}

void xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_fini_function(void * message_memory)
{
  xycar_msgs__msg__XycarUltrasonic__fini(message_memory);
}

size_t xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__size_function__XycarUltrasonic__ranges(
  const void * untyped_member)
{
  const sensor_msgs__msg__Range__Sequence * member =
    (const sensor_msgs__msg__Range__Sequence *)(untyped_member);
  return member->size;
}

const void * xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_const_function__XycarUltrasonic__ranges(
  const void * untyped_member, size_t index)
{
  const sensor_msgs__msg__Range__Sequence * member =
    (const sensor_msgs__msg__Range__Sequence *)(untyped_member);
  return &member->data[index];
}

void * xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_function__XycarUltrasonic__ranges(
  void * untyped_member, size_t index)
{
  sensor_msgs__msg__Range__Sequence * member =
    (sensor_msgs__msg__Range__Sequence *)(untyped_member);
  return &member->data[index];
}

void xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__fetch_function__XycarUltrasonic__ranges(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const sensor_msgs__msg__Range * item =
    ((const sensor_msgs__msg__Range *)
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_const_function__XycarUltrasonic__ranges(untyped_member, index));
  sensor_msgs__msg__Range * value =
    (sensor_msgs__msg__Range *)(untyped_value);
  *value = *item;
}

void xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__assign_function__XycarUltrasonic__ranges(
  void * untyped_member, size_t index, const void * untyped_value)
{
  sensor_msgs__msg__Range * item =
    ((sensor_msgs__msg__Range *)
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_function__XycarUltrasonic__ranges(untyped_member, index));
  const sensor_msgs__msg__Range * value =
    (const sensor_msgs__msg__Range *)(untyped_value);
  *item = *value;
}

bool xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__resize_function__XycarUltrasonic__ranges(
  void * untyped_member, size_t size)
{
  sensor_msgs__msg__Range__Sequence * member =
    (sensor_msgs__msg__Range__Sequence *)(untyped_member);
  sensor_msgs__msg__Range__Sequence__fini(member);
  return sensor_msgs__msg__Range__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xycar_msgs__msg__XycarUltrasonic, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "ranges",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xycar_msgs__msg__XycarUltrasonic, ranges),  // bytes offset in struct
    NULL,  // default value
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__size_function__XycarUltrasonic__ranges,  // size() function pointer
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_const_function__XycarUltrasonic__ranges,  // get_const(index) function pointer
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__get_function__XycarUltrasonic__ranges,  // get(index) function pointer
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__fetch_function__XycarUltrasonic__ranges,  // fetch(index, &value) function pointer
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__assign_function__XycarUltrasonic__ranges,  // assign(index, value) function pointer
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__resize_function__XycarUltrasonic__ranges  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_members = {
  "xycar_msgs__msg",  // message namespace
  "XycarUltrasonic",  // message name
  2,  // number of fields
  sizeof(xycar_msgs__msg__XycarUltrasonic),
  xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_member_array,  // message members
  xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_init_function,  // function to initialize message memory (memory has to be allocated)
  xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_type_support_handle = {
  0,
  &xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xycar_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xycar_msgs, msg, XycarUltrasonic)() {
  xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Range)();
  if (!xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_type_support_handle.typesupport_identifier) {
    xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &xycar_msgs__msg__XycarUltrasonic__rosidl_typesupport_introspection_c__XycarUltrasonic_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
