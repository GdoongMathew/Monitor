
from monitor import BasicMonitor
from test_reader import cpu_reader, gpu_reader, reader
import queue
import contextlib
import pytest


@contextlib.contextmanager
def not_raise_error():
    yield


@pytest.mark.parametrize('reader, proto_que, error', [
    ('cpu_reader', queue.Queue(), not_raise_error()),
    ('gpu_reader', queue.Queue(), not_raise_error()),
    ('cpu_reader', None, pytest.raises(TypeError)),
    # (None, queue.Queue(), pytest.raises(TypeError)),
], indirect=['reader'])
def test_monitor_raise_error(reader, proto_que, error):
    with error:
        BasicMonitor(reader, proto_que)
