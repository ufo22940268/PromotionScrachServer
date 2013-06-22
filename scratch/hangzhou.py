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
        return "杭州银行";

    def fetchBankList(self):
        banks = [];
	url = "http://www.hccb.com.cn/xyk/hdgg/index.shtml#";
	soup = self.getSoup(url);
	if not soup:
	    return banks;
	for td in soup.find_all("td", class_="newstitle"):
	    b = Bank();
	    a = td.find("a");
	    b.url = "http://www.hccb.com.cn" + a["href"].encode("utf-8");
	    b.title = self.getTitle(b.url);
	    b.endTime = self.getEndTime(b.url);
	    banks.append(b);

	return banks;

    def getEndTime(self, url):
	soup = self.getSoup(url);
	if soup:
	    m = re.match(r".*至(.*?日)", soup.get_text().encode("utf-8"), re.DOTALL);
	    if m:
		return date_parser.parseChineseStyle(m.group(1));

    def getTitle(self, url):
	soup = self.getSoup(url);
	if soup:
	    m = re.match(r".*活动内容.*?\s+([^\n]*)", soup.get_text().encode("utf-8"), re.DOTALL);
	    if m:
		return m.group(1).strip();
	return "";
