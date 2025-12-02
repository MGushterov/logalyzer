import unittest
from logalyzer.models import *
from datetime import datetime
from logalyzer.parser import parse_line


class TestLogRecord(unittest.TestCase):
    def test_init(self):
        dt = datetime.now()
        lr = LogRecord('192.168.10.21', dt, HTTPMethod.GET, 'C:/UsersANG/PycharmProjects/logalyzer',
                       201, None, 'log')
        self.assertEqual(lr.ip, "192.168.10.21")
        self.assertEqual(lr.status, 201)
        self.assertEqual(lr.method, HTTPMethod.GET)
        self.assertEqual(lr.size, None)
        self.assertEqual(lr.raw, "log")

    def test_is_error(self):
        dt = datetime.now()
        lr = LogRecord('192.168.10.21', dt, HTTPMethod.GET, 'C:/UsersANG/PycharmProjects/logalyzer',
                       404, None, 'log')
        self.assertEqual(lr.is_error(), True)

    def test_status_class(self):
        dt = datetime.now()
        lr = LogRecord('192.168.10.21', dt, HTTPMethod.GET, 'C:/UsersANG/PycharmProjects/logalyzer',
                       404, None, 'log')
        self.assertEqual(lr.status_class, StatusClass.CLIENT_ERROR)


class TestParser(unittest.TestCase):
    def test_parser_apache_combined(self):
        log = ('127.0.0.1 - - [18/Nov/2025:20:11:42 +0200] "GET /api/4MFphOC4P5rY/announcements/1 HTTP/1.1" 200 544 '
               '"https://app.test/announcements/4MFphOC4P5rY/1" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) '
               'Gecko/20100101 Firefox/145.0"')
        lr = parse_line(log, 'apache_combined')
        res = LogRecord('127.0.0.1', datetime.strptime('18/Nov/2025:20:11:42 +0200',
                                                       '%d/%b/%Y:%H:%M:%S %z'), HTTPMethod.GET,
                        '/api/4MFphOC4P5rY/announcements/1', 200, 544, log.rstrip('\n'))
        self.assertEqual(lr, res)


if __name__ == '__main__':
    unittest.main()
