# -*- coding: utf-8 -*-
import unittest
import requests
from mock import MagicMock

from remotestatsclient.monitor import Monitor


class TestMonitor(unittest.TestCase):

    def test_measure(self):
        self.assertRaises(NotImplementedError,
                          Monitor('http://localhost', 'computerA', 5).measure)

    def test_add_sample(self):
        monitor = Monitor('http://localhost', 'computerA', 5)
        monitor._add_sample(10)
        self.assertEquals(monitor.last_samples[-1][1], 10)

    def test_subclasses_measure(self):
        monitors = [m('http://localhost', 'computerA', 5)
                    for m in Monitor.monitors()]
        for m in monitors:
            m.measure()
            self.assertEqual(len(m.last_samples), 1)
            self.assertIsInstance(m.last_samples[-1], list)
            self.assertEqual(len(m.last_samples[-1]), 2)


class SubMonitor(Monitor):
    def __init__(self, *args):
        super(SubMonitor, self).__init__('http://localhost', 'computerA', 5)

    def measure(self):
        return 1

    @property
    def description(self):
        return 'Foo (m/s)'


class TestMonitorSubclass(unittest.TestCase):
    @staticmethod
    def _mock_requests_with_code(code):
        requests.post = MagicMock()
        requests.put = MagicMock()
        return_mock = MagicMock()
        return_mock.status_code = code
        requests.put.return_value = return_mock

    def test_plot_registered_success(self):
        requests.post = MagicMock()
        self.assertTrue(SubMonitor().plot_registered)

    def test_plot_registered_failure(self):
        requests.post = MagicMock(
            side_effect=requests.exceptions.ConnectionError)
        self.assertFalse(SubMonitor().plot_registered)

    def test_flush_200(self):
        self._mock_requests_with_code(200)
        monitor = SubMonitor()
        monitor.last_samples = [[1, 2], [3, 4]]
        monitor.flush()
        self.assertEqual(requests.put.mock_calls[0][2]['json']['measures'],
                         [[1, 2], [3, 4]])
        self.assertEqual(requests.put.mock_calls[0][2]['json']['id'],
                         'SubMonitor_computerA')
        self.assertEqual(monitor.last_samples, [])

    def test_flush_404(self):
        self._mock_requests_with_code(404)
        monitor = SubMonitor()
        monitor.last_samples = [[1, 2], [3, 4]]
        monitor.flush()
        self.assertEqual(requests.put.mock_calls[0][2]['json']['measures'],
                         [[1, 2], [3, 4]])
        self.assertEqual(requests.put.mock_calls[0][2]['json']['id'],
                         'SubMonitor_computerA')
        self.assertEqual(monitor.last_samples, [[1, 2], [3, 4]])

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
