#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class CgbGetter(BaseGetter):
    def getName(self):
        return "广发银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.TEST_PAGE_COUNT): 
            print "page", page
            f = self.openUrl("http://www.cgbchina.com.cn/Channel/11608406?_tp_info=" + str(page));
            if f == None:
                break;

            soup = BeautifulSoup(f);
            lis = soup.find("div", class_="list_content").find_all("div", class_="text");
            for l in lis:
                b = Bank();
                a = l.find("a");
                b.url = "http://www.cgbchina.com.cn" + a["href"].encode("utf-8");
                b.title = l.find("p", class_="red").string.encode("utf-8");
                banks.append(b);
        return banks;
