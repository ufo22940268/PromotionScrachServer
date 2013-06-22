#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser

FIXED_COUNT = 4;
class BanksGetter(BaseGetter):

    def __init__(self):
        self.prevSoup = None;
    
    def getName(self):
        return "上海农商银行";

    def fetchBankList(self):
        banks = [];
	url = "http://www.srcb.com/cardActivity/index.shtml";
	soup = self.getSoup(url);
	if not soup:
	    return banks;

	for ul in soup.find("div", class_="active_list").find_all("ul"):
	    b = Bank();
	    a = ul.find("a");
	    b.url = a["href"].encode("utf-8");
	    b.title = a["title"].encode("utf-8");
	    ds = ul.find("span").string.encode("utf-8");
	    m = re.match(r"至\s+(.*)", ds);
	    if m:
		b.endTime = date_parser.parseDashLineStyle(m.group(1));
	    banks.append(b);

	return banks;
