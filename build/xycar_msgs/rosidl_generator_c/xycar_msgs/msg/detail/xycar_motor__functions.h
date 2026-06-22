// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice

#ifndef XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__FUNCTIONS_H_
#define XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "xycar_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "xycar_msgs/msg/detail/xycar_motor__struct.h"

/// Initialize msg/XycarMotor message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * xycar_msgs__msg__XycarMotor
 * )) before or use
 * xycar_msgs__msg__XycarMotor__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__init(xycar_msgs__msg__XycarMotor * msg);

/// Finalize msg/XycarMotor message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
void
xycar_msgs__msg__XycarMotor__fini(xycar_msgs__msg__XycarMotor * msg);

/// Create msg/XycarMotor message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * xycar_msgs__msg__XycarMotor__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
xycar_msgs__msg__XycarMotor *
xycar_msgs__msg__XycarMotor__create();

/// Destroy msg/XycarMotor message.
/**
 * It calls
 * xycar_msgs__msg__XycarMotor__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
void
xycar_msgs__msg__XycarMotor__destroy(xycar_msgs__msg__XycarMotor * msg);

/// Check for msg/XycarMotor message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__are_equal(const xycar_msgs__msg__XycarMotor * lhs, const xycar_msgs__msg__XycarMotor * rhs);

/// Copy a msg/XycarMotor message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__copy(
  const xycar_msgs__msg__XycarMotor * input,
  xycar_msgs__msg__XycarMotor * output);

/// Initialize array of msg/XycarMotor messages.
/**
 * It allocates the memory for the number of elements and calls
 * xycar_msgs__msg__XycarMotor__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__Sequence__init(xycar_msgs__msg__XycarMotor__Sequence * array, size_t size);

/// Finalize array of msg/XycarMotor messages.
/**
 * It calls
 * xycar_msgs__msg__XycarMotor__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
void
xycar_msgs__msg__XycarMotor__Sequence__fini(xycar_msgs__msg__XycarMotor__Sequence * array);

/// Create array of msg/XycarMotor messages.
/**
 * It allocates the memory for the array and calls
 * xycar_msgs__msg__XycarMotor__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
xycar_msgs__msg__XycarMotor__Sequence *
xycar_msgs__msg__XycarMotor__Sequence__create(size_t size);

/// Destroy array of msg/XycarMotor messages.
/**
 * It calls
 * xycar_msgs__msg__XycarMotor__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
void
xycar_msgs__msg__XycarMotor__Sequence__destroy(xycar_msgs__msg__XycarMotor__Sequence * array);

/// Check for msg/XycarMotor message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__Sequence__are_equal(const xycar_msgs__msg__XycarMotor__Sequence * lhs, const xycar_msgs__msg__XycarMotor__Sequence * rhs);

/// Copy an array of msg/XycarMotor messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_xycar_msgs
bool
xycar_msgs__msg__XycarMotor__Sequence__copy(
  const xycar_msgs__msg__XycarMotor__Sequence * input,
  xycar_msgs__msg__XycarMotor__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // XYCAR_MSGS__MSG__DETAIL__XYCAR_MOTOR__FUNCTIONS_H_
