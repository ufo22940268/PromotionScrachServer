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
        return "上海银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://www.bankofshanghai.com/servlet/ServletGate?op=Forward&cur_page=MorePage&target=more&systemModule=1104&cid=110404&page=%d&menuId=&navigation=-%20%25D2%25F8%25D0%25D0%25BF%25A8%25D2%25B5%25CE%25F1%25B6%25AF%25CC%25AC"
        for p in range(1, self.getPageRange()):
            url = "http://www.bankofshanghai.com/servlet/ServletGate?op=Forward&cur_page=MorePage&target=more&systemModule=1104&cid=110404&page=" + str(p) +"&menuId=&navigation=-%20%25D2%25F8%25D0%25D0%25BF%25A8%25D2%25B5%25CE%25F1%25B6%25AF%25CC%25AC"
            soup = self.getSoup(url);
            if not soup or self.isSoupEquals(soup, self.prevSoup):
                break;

            self.prevSoup = soup;
            for td in soup.find_all("td", bgcolor="#F5F5F5", width="71%"):
                b = Bank();
                a = td.find("a");
                if not a:
                    continue;

                b.url = "http://www.bankofshanghai.com/" + a["href"].encode("utf-8");
                b.title = a["title"].encode("utf-8");
                banks.append(b);

	return banks;
