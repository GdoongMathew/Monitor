# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='device.proto',
  package='device',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x64\x65vice.proto\x12\x06\x64\x65vice\"7\n\nMemoryInfo\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0c\n\x04\x66ree\x18\x02 \x01(\x03\x12\x0c\n\x04used\x18\x03 \x01(\x03\"F\n\x0bTemperature\x12\x11\n\x07\x43\x65lsius\x18\x01 \x01(\x02H\x00\x12\x14\n\nFahrenheit\x18\x02 \x01(\x02H\x00\x42\x0e\n\x0ctemp_reading\"C\n\x07Process\x12\x0b\n\x03pid\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06memory\x18\x03 \x01(\x03\x12\r\n\x05usage\x18\x04 \x01(\x02\"k\n\tBasicInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x05\x12\x0e\n\x06serial\x18\x03 \x01(\t\x12\x0c\n\x04uuid\x18\x04 \x01(\t\x12\x14\n\x0c\x61rchitecture\x18\x05 \x01(\t\x12\r\n\x05\x62rand\x18\x06 \x01(\t\"\xa6\x01\n\nMatrixInfo\x12(\n\x0btemperature\x18\x01 \x01(\x0b\x32\x13.device.Temperature\x12\'\n\x0bmemory_info\x18\x02 \x01(\x0b\x32\x12.device.MemoryInfo\x12\r\n\x05usage\x18\x03 \x01(\x02\x12\x14\n\x0cmemory_usage\x18\x04 \x01(\x02\x12 \n\x07process\x18\x05 \x03(\x0b\x32\x0f.device.Process\"\x91\x01\n\x05NVGPU\x12\x1f\n\x04info\x18\x01 \x01(\x0b\x32\x11.device.BasicInfo\x12\"\n\x06matrix\x18\x02 \x01(\x0b\x32\x12.device.MatrixInfo\x12\x14\n\x0c\x63uda_version\x18\x03 \x01(\x05\x12\x15\n\rcuda_capacity\x18\x04 \x01(\t\x12\x16\n\x0e\x64river_version\x18\x05 \x01(\t\"+\n\nNVGPUArray\x12\x1d\n\x06nvg_pu\x18\x01 \x03(\x0b\x32\r.device.NVGPU\"J\n\x03\x43PU\x12\x1f\n\x04info\x18\x01 \x01(\x0b\x32\x11.device.BasicInfo\x12\"\n\x06matrix\x18\x02 \x01(\x0b\x32\x12.device.MatrixInfob\x06proto3'
)




_MEMORYINFO = _descriptor.Descriptor(
  name='MemoryInfo',
  full_name='device.MemoryInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='device.MemoryInfo.total', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='free', full_name='device.MemoryInfo.free', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='used', full_name='device.MemoryInfo.used', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=79,
)


_TEMPERATURE = _descriptor.Descriptor(
  name='Temperature',
  full_name='device.Temperature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Celsius', full_name='device.Temperature.Celsius', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Fahrenheit', full_name='device.Temperature.Fahrenheit', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='temp_reading', full_name='device.Temperature.temp_reading',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=81,
  serialized_end=151,
)


_PROCESS = _descriptor.Descriptor(
  name='Process',
  full_name='device.Process',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pid', full_name='device.Process.pid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='device.Process.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory', full_name='device.Process.memory', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='usage', full_name='device.Process.usage', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=153,
  serialized_end=220,
)


_BASICINFO = _descriptor.Descriptor(
  name='BasicInfo',
  full_name='device.BasicInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='device.BasicInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index', full_name='device.BasicInfo.index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serial', full_name='device.BasicInfo.serial', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='device.BasicInfo.uuid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='architecture', full_name='device.BasicInfo.architecture', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='brand', full_name='device.BasicInfo.brand', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=222,
  serialized_end=329,
)


_MATRIXINFO = _descriptor.Descriptor(
  name='MatrixInfo',
  full_name='device.MatrixInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='temperature', full_name='device.MatrixInfo.temperature', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory_info', full_name='device.MatrixInfo.memory_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='usage', full_name='device.MatrixInfo.usage', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory_usage', full_name='device.MatrixInfo.memory_usage', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='process', full_name='device.MatrixInfo.process', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=332,
  serialized_end=498,
)


_NVGPU = _descriptor.Descriptor(
  name='NVGPU',
  full_name='device.NVGPU',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='device.NVGPU.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='matrix', full_name='device.NVGPU.matrix', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cuda_version', full_name='device.NVGPU.cuda_version', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cuda_capacity', full_name='device.NVGPU.cuda_capacity', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='driver_version', full_name='device.NVGPU.driver_version', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=501,
  serialized_end=646,
)


_NVGPUARRAY = _descriptor.Descriptor(
  name='NVGPUArray',
  full_name='device.NVGPUArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nvg_pu', full_name='device.NVGPUArray.nvg_pu', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=648,
  serialized_end=691,
)


_CPU = _descriptor.Descriptor(
  name='CPU',
  full_name='device.CPU',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='device.CPU.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='matrix', full_name='device.CPU.matrix', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=693,
  serialized_end=767,
)

_TEMPERATURE.oneofs_by_name['temp_reading'].fields.append(
  _TEMPERATURE.fields_by_name['Celsius'])
_TEMPERATURE.fields_by_name['Celsius'].containing_oneof = _TEMPERATURE.oneofs_by_name['temp_reading']
_TEMPERATURE.oneofs_by_name['temp_reading'].fields.append(
  _TEMPERATURE.fields_by_name['Fahrenheit'])
_TEMPERATURE.fields_by_name['Fahrenheit'].containing_oneof = _TEMPERATURE.oneofs_by_name['temp_reading']
_MATRIXINFO.fields_by_name['temperature'].message_type = _TEMPERATURE
_MATRIXINFO.fields_by_name['memory_info'].message_type = _MEMORYINFO
_MATRIXINFO.fields_by_name['process'].message_type = _PROCESS
_NVGPU.fields_by_name['info'].message_type = _BASICINFO
_NVGPU.fields_by_name['matrix'].message_type = _MATRIXINFO
_NVGPUARRAY.fields_by_name['nvg_pu'].message_type = _NVGPU
_CPU.fields_by_name['info'].message_type = _BASICINFO
_CPU.fields_by_name['matrix'].message_type = _MATRIXINFO
DESCRIPTOR.message_types_by_name['MemoryInfo'] = _MEMORYINFO
DESCRIPTOR.message_types_by_name['Temperature'] = _TEMPERATURE
DESCRIPTOR.message_types_by_name['Process'] = _PROCESS
DESCRIPTOR.message_types_by_name['BasicInfo'] = _BASICINFO
DESCRIPTOR.message_types_by_name['MatrixInfo'] = _MATRIXINFO
DESCRIPTOR.message_types_by_name['NVGPU'] = _NVGPU
DESCRIPTOR.message_types_by_name['NVGPUArray'] = _NVGPUARRAY
DESCRIPTOR.message_types_by_name['CPU'] = _CPU
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MemoryInfo = _reflection.GeneratedProtocolMessageType('MemoryInfo', (_message.Message,), {
  'DESCRIPTOR' : _MEMORYINFO,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.MemoryInfo)
  })
_sym_db.RegisterMessage(MemoryInfo)

Temperature = _reflection.GeneratedProtocolMessageType('Temperature', (_message.Message,), {
  'DESCRIPTOR' : _TEMPERATURE,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.Temperature)
  })
_sym_db.RegisterMessage(Temperature)

Process = _reflection.GeneratedProtocolMessageType('Process', (_message.Message,), {
  'DESCRIPTOR' : _PROCESS,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.Process)
  })
_sym_db.RegisterMessage(Process)

BasicInfo = _reflection.GeneratedProtocolMessageType('BasicInfo', (_message.Message,), {
  'DESCRIPTOR' : _BASICINFO,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.BasicInfo)
  })
_sym_db.RegisterMessage(BasicInfo)

MatrixInfo = _reflection.GeneratedProtocolMessageType('MatrixInfo', (_message.Message,), {
  'DESCRIPTOR' : _MATRIXINFO,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.MatrixInfo)
  })
_sym_db.RegisterMessage(MatrixInfo)

NVGPU = _reflection.GeneratedProtocolMessageType('NVGPU', (_message.Message,), {
  'DESCRIPTOR' : _NVGPU,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.NVGPU)
  })
_sym_db.RegisterMessage(NVGPU)

NVGPUArray = _reflection.GeneratedProtocolMessageType('NVGPUArray', (_message.Message,), {
  'DESCRIPTOR' : _NVGPUARRAY,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.NVGPUArray)
  })
_sym_db.RegisterMessage(NVGPUArray)

CPU = _reflection.GeneratedProtocolMessageType('CPU', (_message.Message,), {
  'DESCRIPTOR' : _CPU,
  '__module__' : 'device_pb2'
  # @@protoc_insertion_point(class_scope:device.CPU)
  })
_sym_db.RegisterMessage(CPU)


# @@protoc_insertion_point(module_scope)