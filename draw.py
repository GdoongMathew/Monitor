import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from monitor import BasicMonitor

style.use('fivethirtyeight')


class _Plot(animation.TimedAnimation):
    def __init__(self, monitor, apply_func=None, main_fig=plt.figure(), subplot_args=(1, 1, 1), interval=1):
        assert isinstance(monitor, BasicMonitor)
        assert callable(apply_func) or isinstance(apply_func, type(None))
        self.monitor = monitor
        self._apply_func = apply_func
        self.sub_plot = main_fig.add_subplot(*subplot_args)
        self.interval = interval
        super(_Plot, self).__init__(main_fig, interval=interval, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        if self.monitor.proto_que.qsize():
            proto = self.monitor.proto_que.get()
            self.plot(proto)

    def plot(self, proto, *args):
        raise NotImplementedError


class PiePlot(_Plot):
    def __init__(self, *args, **kwargs):
        super(PiePlot, self).__init__(*args, **kwargs)

    def plot(self, proto, *args):
        # pre_process the proto data
        if callable(self._apply_func):
            data = self._apply_func(proto)
        else:
            data = proto
        self.sub_plot.pie(data)


class LinePlot(_Plot):
    def __init__(self, *args, **kwargs):
        super(LinePlot, self).__init__(*args, **kwargs)

    def plot(self, proto, *args):
        if callable(self._apply_func):
            data = self._apply_func(proto)
        else:
            data = proto
        self.sub_plot.plot(data)

