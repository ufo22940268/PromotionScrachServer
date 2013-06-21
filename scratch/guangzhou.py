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

class BanksGetter(BaseGetter):
    def getName(self):
        return "广州银行";

    def fetchBankList(self):
        banks = [];
	soup = self.getSoup("http://creditcard.gzcb.com.cn/Activities3.html", encoding="gbk");
	if not soup:
	    return banks;

	for a in soup.find("div", class_="active_C").find("ul").find_all("a"):
	    b = Bank();
	    b.url = "http://creditcard.gzcb.com.cn/" + a["href"].encode("utf-8");
	    b.title = a.string.encode("utf-8");
	    banks.append(b);

	return banks;
