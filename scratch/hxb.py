#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser

class BanksGetter(BaseGetter):
    def getName(self):
        return "华夏银行";

    def fetchBankList(self):
	prefUrls = ["http://creditcard.hxb.com.cn/hotnews/index.jsp?cid=12347700871250001", "http://creditcard.hxb.com.cn/hotnews/index.jsp?cid=12347701281290003"];
        banks = [];
	for prefUrl in prefUrls:
	    for page in range(0, self.getPageRange()): 
		url = prefUrl + "&page_count=30&page_start=%d" % (page*5);
		soup = self.getSoup(url);
		lis = soup.find_all("div", id="rm_lcd");
		for l in lis:
		    b = Bank();
		    a = l.find("a");
		    b.url = "http://creditcard.hxb.com.cn" + a["href"].encode("utf-8");
		    b.title = a["title"].encode("utf-8").strip();
		    h6 = l.find("h6").string;
                    if h6 != None:
                        m = re.match("\[.*至(.*)\]", h6.encode("utf-8"));
                        if m != None:
                            b.endDate = date_parser.parseDashLineStyle(m.group(1));
		    banks.append(b);

	return banks;
