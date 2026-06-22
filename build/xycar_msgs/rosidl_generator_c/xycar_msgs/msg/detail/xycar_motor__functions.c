// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from xycar_msgs:msg/XycarMotor.idl
// generated code does not contain a copyright notice
#include "xycar_msgs/msg/detail/xycar_motor__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
xycar_msgs__msg__XycarMotor__init(xycar_msgs__msg__XycarMotor * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    xycar_msgs__msg__XycarMotor__fini(msg);
    return false;
  }
  // angle
  // speed
  return true;
}

void
xycar_msgs__msg__XycarMotor__fini(xycar_msgs__msg__XycarMotor * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // angle
  // speed
}

bool
xycar_msgs__msg__XycarMotor__are_equal(const xycar_msgs__msg__XycarMotor * lhs, const xycar_msgs__msg__XycarMotor * rhs)
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
  // angle
  if (lhs->angle != rhs->angle) {
    return false;
  }
  // speed
  if (lhs->speed != rhs->speed) {
    return false;
  }
  return true;
}

bool
xycar_msgs__msg__XycarMotor__copy(
  const xycar_msgs__msg__XycarMotor * input,
  xycar_msgs__msg__XycarMotor * output)
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
  // angle
  output->angle = input->angle;
  // speed
  output->speed = input->speed;
  return true;
}

xycar_msgs__msg__XycarMotor *
xycar_msgs__msg__XycarMotor__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarMotor * msg = (xycar_msgs__msg__XycarMotor *)allocator.allocate(sizeof(xycar_msgs__msg__XycarMotor), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xycar_msgs__msg__XycarMotor));
  bool success = xycar_msgs__msg__XycarMotor__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xycar_msgs__msg__XycarMotor__destroy(xycar_msgs__msg__XycarMotor * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xycar_msgs__msg__XycarMotor__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xycar_msgs__msg__XycarMotor__Sequence__init(xycar_msgs__msg__XycarMotor__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarMotor * data = NULL;

  if (size) {
    data = (xycar_msgs__msg__XycarMotor *)allocator.zero_allocate(size, sizeof(xycar_msgs__msg__XycarMotor), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xycar_msgs__msg__XycarMotor__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xycar_msgs__msg__XycarMotor__fini(&data[i - 1]);
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
xycar_msgs__msg__XycarMotor__Sequence__fini(xycar_msgs__msg__XycarMotor__Sequence * array)
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
      xycar_msgs__msg__XycarMotor__fini(&array->data[i]);
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

xycar_msgs__msg__XycarMotor__Sequence *
xycar_msgs__msg__XycarMotor__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xycar_msgs__msg__XycarMotor__Sequence * array = (xycar_msgs__msg__XycarMotor__Sequence *)allocator.allocate(sizeof(xycar_msgs__msg__XycarMotor__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xycar_msgs__msg__XycarMotor__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xycar_msgs__msg__XycarMotor__Sequence__destroy(xycar_msgs__msg__XycarMotor__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xycar_msgs__msg__XycarMotor__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xycar_msgs__msg__XycarMotor__Sequence__are_equal(const xycar_msgs__msg__XycarMotor__Sequence * lhs, const xycar_msgs__msg__XycarMotor__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xycar_msgs__msg__XycarMotor__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xycar_msgs__msg__XycarMotor__Sequence__copy(
  const xycar_msgs__msg__XycarMotor__Sequence * input,
  xycar_msgs__msg__XycarMotor__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xycar_msgs__msg__XycarMotor);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xycar_msgs__msg__XycarMotor * data =
      (xycar_msgs__msg__XycarMotor *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xycar_msgs__msg__XycarMotor__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xycar_msgs__msg__XycarMotor__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xycar_msgs__msg__XycarMotor__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
