# -*- coding: utf-8 -*-
import time
import psutil
import requests


class Monitor(object):
    def __init__(self, server, hostname, interval):
        self.server = server
        self.hostname = hostname
        self.interval = interval
        self.last_samples = []
        self.id = type(self).__name__ + '_' + hostname
        self._plot_registered = False

    @staticmethod
    def monitors():
        """List all monitors in this module."""
        def all_subclasses(cls):
            sub_classes = cls.__subclasses__()
            return sub_classes + [g for s in cls.__subclasses__()
                                  for g in all_subclasses(s)]
        current_module = __name__
        monitor_classes = all_subclasses(Monitor)
        monitor_classes = filter(lambda x: x.__module__ == current_module,
                                 monitor_classes)
        return monitor_classes

    def measure(self):
        """Measure a datapoint and stores it in the last_samples list."""
        raise NotImplementedError("measure must be implemented in a subclass")

    def flush(self):
        """Tries to send the last samples to the server."""
        if self.plot_registered:
            try:
                r = requests.put(self.server, json={
                    'id': self.id, 'measures': self.last_samples})
            except requests.exceptions.RequestException:
                return
            if r.status_code == 200:
                self.last_samples = []
            elif r.status_code == 404:
                self._plot_registered = False

    def _add_sample(self, value):
        current_time = int(time.time()*1000)
        sample = [current_time, value]
        self.last_samples.append(sample)

    @property
    def plot_registered(self):
        if not self._plot_registered:
            req_json = {'id': self.id,
                        'hostname': self.hostname,
                        'description': self.description,
                        'interval': self.interval*1000}
            try:
                requests.post(self.server, json=req_json)
            except requests.exceptions.RequestException:
                return False
            else:
                self._plot_registered = True
        return self._plot_registered

    @property
    def description(self):
        raise NotImplementedError("description must be implemented in a"
                                  "subclass")


class MemoryMonitor(Monitor):
    def measure(self):
        self._add_sample(psutil.virtual_memory().percent)

    @property
    def description(self):
        return 'Memory (%)'


class CpuMonitor(Monitor):
    def measure(self):
        self._add_sample(psutil.cpu_percent())

    @property
    def description(self):
        return 'CPU (%)'
