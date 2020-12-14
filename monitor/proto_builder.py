from device_pb2 import *


class ProtoBuilder:
    proto = None

    @classmethod
    def _build_proto(cls, **kwargs):
        assert callable(cls.proto)
        proto = cls.proto()
        for key, item in kwargs.items():
            if key in proto.DESCRIPTOR.fields_by_name and item is not None:
                _field = getattr(proto, key)
                if hasattr(_field, 'CopyFrom'):
                    _field.CopyFrom(item)
                elif isinstance(item, (list, set, tuple)):
                    _field.extend(item)
                else:
                    setattr(proto, key, item)

        return proto

    @classmethod
    def build_proto(cls, **kwargs):
        raise NotImplementedError


class TemperatureProtoBuilder(ProtoBuilder):
    proto = Temperature

    @classmethod
    def build_proto(cls, temperature=None, **kwargs):
        if temperature is None:
            temperature = dict()
        return cls._build_proto(**temperature)


class MemoryInfoProtoBuilder(ProtoBuilder):
    proto = MemoryInfo

    @classmethod
    def build_proto(cls, total=None, free=None, used=None, **kwargs):
        return cls._build_proto(total=total, free=free, used=used)


class ProcessProtoBuilder(ProtoBuilder):
    proto = Process

    @classmethod
    def build_proto(cls, pid=None, name=None, memory=None, usage=None, **kwargs):
        return cls._build_proto(pid=pid, name=name, memory=memory, usage=usage)


class RepeatedProcessProtoBuilder(ProtoBuilder):

    @classmethod
    def build_proto(cls, process=None, **kwargs):
        _proto_list = []
        if process is not None:
            for proc_item in process:
                _proto_list.append(cls._build_proto(**proc_item))
        return _proto_list


class BasicInfoProtoBuilder(ProtoBuilder):
    proto = BasicInfo

    @classmethod
    def build_proto(cls, name=None, index=None, serial=None, uuid=None, architecture=None, brand=None, **kwargs):
        return cls._build_proto(name=name,
                                index=index,
                                serial=serial,
                                uuid=uuid,
                                architecture=architecture,
                                brand=brand)


class MatrixInfoProtoBuilder(ProtoBuilder):
    proto = MatrixInfo

    @classmethod
    def build_proto(cls, usage=None, memory_usage=None, **kwargs):
        temp_proto = TemperatureProtoBuilder.build_proto(**kwargs)
        memory_proto = MemoryInfoProtoBuilder.build_proto(**kwargs)
        proc_proto_list = RepeatedProcessProtoBuilder.build_proto(**kwargs)
        return cls._build_proto(temperature=temp_proto,
                                memory_info=memory_proto,
                                usage=usage,
                                memory_usage=memory_usage,
                                process=proc_proto_list)


class NVGPUProtoBuilder(ProtoBuilder):
    proto = NVGPU

    @classmethod
    def build_proto(cls, cuda_version=None, cuda_capacity=None,
                    driver_version=None, **kwargs):
        info_proto = BasicInfoProtoBuilder.build_proto(**kwargs)
        matrix_proto = MatrixInfoProtoBuilder.build_proto(**kwargs)
        return cls._build_proto(info=info_proto,
                                matrix=matrix_proto,
                                cuda_version=cuda_version,
                                cuda_capacity=cuda_capacity,
                                driver_version=driver_version)


class CPUProtoBuilder(ProtoBuilder):
    proto = CPU

    @classmethod
    def build_proto(cls, **kwargs):
        info_proto = BasicInfoProtoBuilder.build_proto(**kwargs)
        matrix_proto = MatrixInfoProtoBuilder.build_proto(**kwargs)
        return cls._build_proto(info=info_proto, matrix=matrix_proto)
