#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "建设银行";

    def fetchBankList(self):
        banks = [];
	for page in range(1, self.TEST_PAGE_COUNT): 
	    f = self.openUrl("http://creditcard.ccb.com/ccapp/doSearch.do?type=bizSearch&s_cityid=0&s_provinceid=0&s_cateid=20100311_1268310067&s_catechildid=&s_lifeid=&pageNo=" + str(page) + "&s_searchKey=");
	    if f == None:
		break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("dl", class_="cont-list");
	    for l in lis:
		b = Bank();
		a = l.find("a");
		b.url = "http://creditcard.ccb.com" + l.find("a", class_="more")["href"].encode("utf-8");
		b.title = l.contents[-2].contents[-1].string.encode("utf-8").strip();
		banks.append(b);
	return banks;