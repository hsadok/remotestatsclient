# -*- coding: utf-8 -*-
import time

from monitor import Monitor


class RemoteStatsClient(object):
    def __init__(self, server, hostname, interval):
        self.server = server
        self.hostname = hostname
        self.interval = interval

    def run(self):
        monitors = [m(self.server, self.hostname, self.interval)
                    for m in Monitor.monitors()]
        while True:
            start_time = time.time()

            map(lambda x: x.measure(), monitors)
            map(lambda x: x.flush(), monitors)

            time_wait = start_time + self.interval - time.time()
            time.sleep(time_wait if time_wait > 0 else 0)
