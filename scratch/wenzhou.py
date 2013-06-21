#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser
import soup_util

FIXED_COUNT = 3;
#TODO Not finished yet.
class BanksGetter(BaseGetter):
    def getName(self):
        return "温州银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://www.wzbank.cn/credit/newslist/menu_item_id/268/page/%d";

        for page in range(1, FIXED_COUNT):
            url = baseUrl % page;
            soup = self.getSoup(url);
            if not soup:
                break;

            for l in soup.find("div", class_="all-news-right-wrapper").find("ul").find_all("li"):
                b = Bank();
                a = l.find("a");
                b.title = a.string.encode("utf-8");
                b.url = "http://www.wzbank.cn" + a["href"].encode("utf-8");
                banks.append(b);

	return banks;

    #TODO Not function well.
    def parseDate(self, url):
	soup = self.getSoup(url);
	if not soup:
	    return;

	print "get_text", soup.get_text().encode("utf-8");
	test = "asdfasdfji至12月2日dfajisdfjiajdf";
	m = re.match(r".*(活动时间)", test);
	if m:
	    print m.group(1);
	    return m.group(1);
	
