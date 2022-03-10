from .reader.device_reader import DeviceReader
import threading
import time
import queue


class BasicMonitor:
    def __init__(self, reader, proto_que=queue.Queue(), interval=0.5):
        if not isinstance(reader, DeviceReader):
            raise TypeError(f'reader should be a type of DeviceReader, get {type(reader)}.')

        if not hasattr(proto_que, 'put') or not callable(proto_que.put):
            raise TypeError('proto_que should has callable put attribute.')
        self.reader = reader
        self.stop_event = threading.Event()
        self.proto_que = proto_que
        self.interval = interval
        self._thd = threading.Thread(target=self.monitor)
        self.proto = self.get_proto(basic_info=True, matrix_info=True)

    def get_proto(self, **kwargs):
        proto = self.reader.to_proto(**kwargs)
        return proto

    def monitor(self):
        t_start = time.time()
        while not self.stop_event.is_set():
            if time.time() - t_start >= self.interval:
                proto = self.get_proto(basic_info=False, matrix_info=True)
                self.proto.matrix.CopyFrom(proto.matrix)
                self.proto_que.put(self.proto)

    def start(self):
        self.stop_event.clear()
        self._thd.start()

    def stop(self):
        self.stop_event.set()
        self._thd.join()
