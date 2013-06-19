#coding=utf-8
import city_parser
import date_parser
import unittest
from datetime import datetime

class ParserTestCase(unittest.TestCase):

    def test_city_parser(self):
	s1 = "中信倍精彩活动[上海]";
	s2 = "[上海]中信倍精彩活动";
	s3 = None;

	self.assertEqual("上海", city_parser.parseBracketStyle(s1));
	self.assertEqual("上海", city_parser.parseBracketStyle(s2));
	self.assertEqual(None, city_parser.parseBracketStyle(s3));

    def test_date_parser(self):
        s1 = "2013-01-01至2013-12-31";
        
        ed = datetime(year=2013, month=12, day=31);
        self.assertEqual(ed, date_parser.parseZhiStyle(s1));
