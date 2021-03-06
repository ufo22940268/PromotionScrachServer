#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re

class BanksGetter(BaseGetter):

	def getName(self):
		return "光大银行";

	def fetchBankList(self):
		banks = [];
		baseUrls = ["http://xyk.cebbank.com/home/activities/category/a_region_dd/list%d.htm","http://xyk.cebbank.com/home/activities/category/a_life_cycle/list%d.htm",];
		print baseUrls;
		for bu in baseUrls:
			for page in range(1, self.getPageRange()): 
				##url = "http://xyk.cebbank.com/home/activities/category/a_life_cycle/list%d.htm" % page;
				url = bu % page;
				soup = self.getSoup(url);
				if not self.isValidSoup(soup):
					break;

				lis = soup.find("ul", class_="th_list_ul").find_all("div", class_="floatleft");
				for l in lis:
					b = Bank();
					a = l.find("a");
					b.url = "http://xyk.cebbank.com" + a["href"].encode("utf-8");
					title = a.string.encode("utf-8").strip();
					m = re.match(r"(.*?)（(.*)）", title);
					if m:
						b.title = m.group(1);
						b.city = m.group(2);
					else:
						b.title = title;
					banks.append(b);
		return banks;

	def isValidSoup(self, soup):
		if soup and soup.get_text().encode("utf-8").find("出错啦") == -1:
			return True;
		else:
			return False;

