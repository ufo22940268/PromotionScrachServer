#coding=utf-8
import city_parser
import unittest
import db

class DbTestCase(unittest.TestCase):

    def testGetCityId(self):
	city = "杭州"

	id = db.getCityId(city);
	self.assertEqual(id, db.getCityId(city));

	city2 = "上海";
	self.assertNotEqual(id, db.getCityId(city2));
