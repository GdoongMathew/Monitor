from reader.device_reader import DeviceReader
import threading
import time
import queue


class BasicMonitor:
    def __init__(self, reader, proto_que=queue.Queue(), interval=0.5):
        assert isinstance(reader, DeviceReader)
        assert hasattr(proto_que, 'put')
        self.reader = reader
        self.stop_event = threading.Event()
        self.proto_que = proto_que
        self.interval = interval
        self._thd = threading.Thread(target=self.monitor)

    def get_proto(self, **kwargs):
        proto = self.reader.to_proto(**kwargs)
        return proto

    def monitor(self):
        t_start = time.time()
        first_time = True
        proto = None
        while not self.stop_event.is_set():
            if time.time() - t_start >= self.interval:
                if first_time:
                    proto = self.get_proto(basic_info=True,
                                           matrix_info=True)

                else:
                    _tmp_proto = self.get_proto(basic_info=False,
                                                matrix_info=True)
                    print(_tmp_proto)
                return proto

    def start(self):
        self.stop_event.clear()
        self._thd.start()

    def stop(self):
        self.stop_event.set()
