#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util
import re

class BanksGetter(BaseGetter):

    def __init__(self):
	self.prevSoup = None;

    def getName(self):
        return "民生银行";

    def fetchBankList(self):
	banks = [];
	baseUrl = "http://creditcard.cmbc.com.cn/promotioninfo/PromotionInfoList.aspx?page=%d";
	for page in range(1, self.getPageRange()):
	    url = baseUrl % page;
	    soup = self.getSoup(url, encoding="gbk"); 

	    if not soup or(self.prevSoup and soup.get_text() == self.prevSoup.get_text()):
		break;

	    self.prevSoup = soup;
	    for l in soup.find_all("li", class_="lb_white"):
		a = l.find("a");
		b = Bank();
		b.title = a["title"].encode("utf-8");
		b.url = "http://creditcard.cmbc.com.cn/promotioninfo/" + a["href"].encode("utf-8");
		b.city = a.next_sibling.string.encode("utf-8");
		banks.append(b);

	return banks;
