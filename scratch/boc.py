#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re

#TODO Can't find the right website.
class BanksGetter(BaseGetter):
    def getName(self):
        return "中国银行";

    def fetchBankList(self):
        banks = [];
        banks += self.getBankListByUrl("http://www.boc.cn/bcservice/bi3/bi31/");
        banks += self.getBankListByUrl("http://www.boc.cn/bcservice/bi3/bi32/");
        return banks;

    def getBankListByUrl(self, url):
        banks = [];

        soup = self.getSoup(url);
        if not soup:
            return;
        lis = soup.find("table", width="550").find_all("a");
        for a in lis:
            b = Bank();
	    b.url = url + a["href"].encode("utf-8");
            title = a.string.encode("utf-8");
            b.title = re.sub("[\[\(](.*)[\]\)]", "", title);
            m = re.match("[\[\(](.*?)[\]\)]", title);
            if m:
                s = m.group(1);
                if s:
                    if s == "已结束":
                        continue
                    else:
                        b.city = s;
            banks.append(b);
        return banks;
