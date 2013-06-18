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
    def getName(self):
        return "浦发银行";

    def fetchBankList(self):
        banks = [];
        banks += self.getBanksByUrl("http://www.spdbccc.com.cn/zh/news1.htm");
        banks += self.getBanksByUrl("http://www.spdbccc.com.cn/zh/news2.htm");
        return banks;

    def getBanksByUrl(self, url):
        banks = [];
        soup = self.getSoup(url);
        if not soup:
            return banks;

        lis = soup.find_all("a", href=re.compile(r"index\.html"));
        for l in lis:
            b = Bank();
            b.url = "http://www.spdbccc.com.cn" + l["href"].encode("utf-8"); 
            b.title = l.string.encode("utf-8");
            banks.append(b);

        return banks;
