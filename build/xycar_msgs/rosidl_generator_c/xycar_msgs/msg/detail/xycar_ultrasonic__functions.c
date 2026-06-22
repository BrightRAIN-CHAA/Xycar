// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from xycar_msgs:msg/XycarUltrasonic.idl
// generated code does not contain a copyright notice
#include "xycar_msgs/msg/detail/xycar_ultrasonic__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `ranges`
#include "sensor_msgs/msg/detail/range__functions.h"

bool
xycar_msgs__msg__XycarUltrasonic__init(xycar_msgs__msg__XycarUltrasonic * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    xycar_msgs__msg__XycarUltrasonic__fini(msg);
    return false;
  }
  // ranges
  if (!sensor_msgs__msg__Range__Sequence__init(&msg->ranges, 0)) {
    xycar_msgs__msg__XycarUltrasonic__fini(msg);
    return false;
  }
  return true;
}

void
xycar_msgs__msg__XycarUltrasonic__fini(xycar_msgs__msg__XycarUltrasonic * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // ranges
  sensor_msgs__msg__Range__Sequence__fini(&msg->ranges);
}

bool
xycar_msgs__msg__XycarUltrasonic__are_equal(const xycar_msgs__msg__XycarUltrasonic * lhs, const xycar_msgs__msg__XycarUltrasonic * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // ranges
  if (!sensor_msgs__msg__Range__Sequence__are_equal(
      &(lhs->ranges), &(rhs->ranges)))
  {
    return false;
  }
  return true;
}

bool
xycar_msgs__msg__XycarUltrasonic__copy(
  const xycar_msgs__msg__XycarUltrasonic * input,
  xycar_msgs__msg__XycarUltrasonic * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // ranges
  if (!sensor_msgs__msg__Range__Sequence__copy(
      &(input->ranges), &(output->ranges)))
  {
    return false;
  }
  return true;
}

xycar_msgs__msg__XycarUltrasonic *
xycar_msgs__msg__XycarUltrasonic__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarUltrasonic * msg = (xycar_msgs__msg__XycarUltrasonic *)allocator.allocate(sizeof(xycar_msgs__msg__XycarUltrasonic), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xycar_msgs__msg__XycarUltrasonic));
  bool success = xycar_msgs__msg__XycarUltrasonic__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xycar_msgs__msg__XycarUltrasonic__destroy(xycar_msgs__msg__XycarUltrasonic * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xycar_msgs__msg__XycarUltrasonic__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xycar_msgs__msg__XycarUltrasonic__Sequence__init(xycar_msgs__msg__XycarUltrasonic__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarUltrasonic * data = NULL;

  if (size) {
    data = (xycar_msgs__msg__XycarUltrasonic *)allocator.zero_allocate(size, sizeof(xycar_msgs__msg__XycarUltrasonic), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xycar_msgs__msg__XycarUltrasonic__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xycar_msgs__msg__XycarUltrasonic__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
xycar_msgs__msg__XycarUltrasonic__Sequence__fini(xycar_msgs__msg__XycarUltrasonic__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      xycar_msgs__msg__XycarUltrasonic__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

xycar_msgs__msg__XycarUltrasonic__Sequence *
xycar_msgs__msg__XycarUltrasonic__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarUltrasonic__Sequence * array = (xycar_msgs__msg__XycarUltrasonic__Sequence *)allocator.allocate(sizeof(xycar_msgs__msg__XycarUltrasonic__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xycar_msgs__msg__XycarUltrasonic__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xycar_msgs__msg__XycarUltrasonic__Sequence__destroy(xycar_msgs__msg__XycarUltrasonic__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xycar_msgs__msg__XycarUltrasonic__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xycar_msgs__msg__XycarUltrasonic__Sequence__are_equal(const xycar_msgs__msg__XycarUltrasonic__Sequence * lhs, const xycar_msgs__msg__XycarUltrasonic__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xycar_msgs__msg__XycarUltrasonic__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xycar_msgs__msg__XycarUltrasonic__Sequence__copy(
  const xycar_msgs__msg__XycarUltrasonic__Sequence * input,
  xycar_msgs__msg__XycarUltrasonic__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xycar_msgs__msg__XycarUltrasonic);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xycar_msgs__msg__XycarUltrasonic * data =
      (xycar_msgs__msg__XycarUltrasonic *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xycar_msgs__msg__XycarUltrasonic__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xycar_msgs__msg__XycarUltrasonic__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xycar_msgs__msg__XycarUltrasonic__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
