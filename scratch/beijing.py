#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import sys
import soup_util

class BanksGetter(BaseGetter):
    def getName(self):
        return "北京银行";

    def fetchBankList(self):
	baseUrl = "http://www.bankofbeijing.com.cn/creditcard/list%s.html";
        banks = [];
	for page in range(1, self.getPageRange()):
	    url = None;
	    if page == 1:
		url = baseUrl % "";
	    else:
		url = baseUrl % "_" + str(page);

	    soup = self.getSoup(url);
	    if not soup:
		break;

	    for a in soup.find("ul", class_="f_000_12").find_all("a"):
		b = Bank();
		b.url = "http://www.bankofbeijing.com.cn" + a["href"].encode("utf-8");
		b.title = a.string.encode("utf-8");
		banks.append(b);

	return banks;
