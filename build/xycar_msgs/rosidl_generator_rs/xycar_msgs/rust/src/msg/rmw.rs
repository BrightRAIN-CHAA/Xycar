#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "xycar_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xycar_msgs__msg__XycarMotor() -> *const std::ffi::c_void;
}

#[link(name = "xycar_msgs__rosidl_generator_c")]
extern "C" {
    fn xycar_msgs__msg__XycarMotor__init(msg: *mut XycarMotor) -> bool;
    fn xycar_msgs__msg__XycarMotor__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<XycarMotor>, size: usize) -> bool;
    fn xycar_msgs__msg__XycarMotor__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<XycarMotor>);
    fn xycar_msgs__msg__XycarMotor__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<XycarMotor>, out_seq: *mut rosidl_runtime_rs::Sequence<XycarMotor>) -> bool;
}

// Corresponds to xycar_msgs__msg__XycarMotor
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XycarMotor {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub angle: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed: f32,

}



impl Default for XycarMotor {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xycar_msgs__msg__XycarMotor__init(&mut msg as *mut _) {
        panic!("Call to xycar_msgs__msg__XycarMotor__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for XycarMotor {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarMotor__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarMotor__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarMotor__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for XycarMotor {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for XycarMotor where Self: Sized {
  const TYPE_NAME: &'static str = "xycar_msgs/msg/XycarMotor";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xycar_msgs__msg__XycarMotor() }
  }
}


#[link(name = "xycar_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xycar_msgs__msg__XycarUltrasonic() -> *const std::ffi::c_void;
}

#[link(name = "xycar_msgs__rosidl_generator_c")]
extern "C" {
    fn xycar_msgs__msg__XycarUltrasonic__init(msg: *mut XycarUltrasonic) -> bool;
    fn xycar_msgs__msg__XycarUltrasonic__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<XycarUltrasonic>, size: usize) -> bool;
    fn xycar_msgs__msg__XycarUltrasonic__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<XycarUltrasonic>);
    fn xycar_msgs__msg__XycarUltrasonic__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<XycarUltrasonic>, out_seq: *mut rosidl_runtime_rs::Sequence<XycarUltrasonic>) -> bool;
}

// Corresponds to xycar_msgs__msg__XycarUltrasonic
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XycarUltrasonic {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub ranges: rosidl_runtime_rs::Sequence<sensor_msgs::msg::rmw::Range>,

}



impl Default for XycarUltrasonic {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xycar_msgs__msg__XycarUltrasonic__init(&mut msg as *mut _) {
        panic!("Call to xycar_msgs__msg__XycarUltrasonic__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for XycarUltrasonic {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarUltrasonic__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarUltrasonic__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xycar_msgs__msg__XycarUltrasonic__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for XycarUltrasonic {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for XycarUltrasonic where Self: Sized {
  const TYPE_NAME: &'static str = "xycar_msgs/msg/XycarUltrasonic";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xycar_msgs__msg__XycarUltrasonic() }
  }
}


