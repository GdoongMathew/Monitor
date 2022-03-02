# Monitor
1. A Hardware reader for reading hardware built-in sensors, hardware usage and memory usage.
2. Currently, only support Nvidia-GPU and CPU.
3. Use Proto3 as the interchange object.

## Usage
```python
from reader import NVGPUReader
reader = NVGPUReader(idx=0)
reader_proto = reader.to_proto(basic_info=True, matrix_info=True)
```

Using monitor:
```python
from reader import NVGPUReader
from monitor import BasicMonitor

gpu_reader = NVGPUReader(idx=0)
monitor = BasicMonitor(gpu_reader)

monitor.start()

while True:
    if monitor.proto_que.qsize():
        proto = monitor.proto_que.get()
        print(proto)
```