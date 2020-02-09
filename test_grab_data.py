import unittest
from grab_data import parse_cmdline, validate_iso8601, \
    validate_station_id, convertHourToChar, generate_url_by_date, download_file_from_ftp
import dateutil.parser

class GrabDataTestCase(unittest.TestCase):
    def test_parse_cmd(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2020-02-08T11:46:25Z"]
        expectStart = dateutil.parser.isoparse(argv[1])
        expectEnd = dateutil.parser.isoparse(argv[2])
        expectRes = (expectStart, expectEnd, argv[0])
        res = parse_cmdline(argv)
        self.assertEqual(res, expectRes)

    def test_parse_cmd_endtime_before_start(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2020-02-07T11:46:25Z"]
        expectRes = ()
        res = parse_cmdline(argv)
        self.assertEqual(res, expectRes)

    def test_parse_cmd_endtime_behind_current(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2021-02-07T11:46:25Z"]
        expectRes = ()
        res = parse_cmdline(argv)
        self.assertEqual(res, expectRes)

    def test_parse_cmd_endtime_behind_current(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2021-02-07T11:46:25Z"]
        expectRes = ()
        res = parse_cmdline(argv)
        self.assertEqual(res, expectRes)

    def test_parse_cmd_argv_morethanfour(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2021-02-07T11:46:25Z", ""]
        expectRes = ()
        res = parse_cmdline(argv)
        self.assertEqual(res, expectRes)

    def test_time_format_true(self):
        argv = "2020-02-08T10:11:24Z"
        res = validate_iso8601(argv)
        self.assertEqual(res, True)

    def test_time_format_False(self):
        argv = "2020-0208T10:11:24Z"
        res = validate_iso8601(argv)
        self.assertEqual(res, False)

    def test_stationID_format_true(self):
        argv = "xyzo"
        res = validate_station_id(argv)
        self.assertEqual(res, True)

    def test_stationID_format_False(self):
        argv = "xyzo2"
        res = validate_station_id(argv)
        self.assertEqual(res, False)

    def test_convertHour(self):
        argv = 20
        res = convertHourToChar(argv)
        self.assertEqual(res, 'u')

    def test_generate_by_date(self):
        argv = ["nybp", "2020-02-08T10:11:24Z", "2020-02-08T11:46:25Z"]
        expectRes = ['2020/039/nybp/nybp039k.20o.gz', '2020/039/nybp/nybp039l.20o.gz']
        startDate = dateutil.parser.isoparse(argv[1])
        endDate = dateutil.parser.isoparse(argv[2])
        res = generate_url_by_date(startDate, endDate, argv[0])
        self.assertEqual(res, expectRes)

    def test_download_file_base_url(self):
        url_list = ['2020/039/nybp/nybp039k.20o.gz', '2020/039/nybp/nybp039l.20o.gz']
        expectRes = ['nybp039k.20o.gz', 'nybp039l.20o.gz']
        res = download_file_from_ftp(url_list)
        self.assertEqual(res, expectRes)

if __name__ == '__main__':
    unittest.main()