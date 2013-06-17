#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "光大银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.getPageRange()): 
	    url = "http://xyk.cebbank.com/home/activities/category/a_life_cycle/list%d.htm" % page;
	    soup = self.getSoup(url);
	    lis = soup.find("ul", class_="th_list_ul").find_all("div", class_="floatleft");
	    for l in lis:
		b = Bank();
		a = l.find("a");
		b.url = "http://xyk.cebbank.com" + a["href"].encode("utf-8");
		b.title = a.string.encode("utf-8").strip();
		banks.append(b);
	return banks;
