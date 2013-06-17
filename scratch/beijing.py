#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import sys
import SoupUtil

class BanksGetter(BaseGetter):
    def getName(self):
        return "北京银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://www.bankofbeijing.com.cn/creditcard/company_%d.html";
        baseUrlWithPage = "http://www.bankofbeijing.com.cn/creditcard/company_%d_%d.html";
        for typeId in range (1, 10): 
            for page in range(1, self.getPageRange()): 
                url = "";
                if page == 1:
                    url = baseUrl % (typeId);
                else:
                    url = baseUrlWithPage % (typeId, page);

                f = self.openUrl(url);
                if f == None:
                    break;

                banks += self.getBanksByUrl(url);

	return banks;

    def getBanksByUrl(self, url):
        print url;
        sys.stdout.flush();
        banks = [];
        f = self.openUrl(url);
        if f == None:
            return banks;

        soup = BeautifulSoup(f);
        lis = soup.find_all("a");
        urls = ["http://www.bankofbeijing.com.cn/" + s["href"].encode("utf-8") for s in lis if s.get("target") != None 
                and s.get("class") == None
                and s["href"].find("/contents") != -1];
        for url in urls:
            b = Bank();
            b.url = url;
            b.title = self.getTitleByUrl(url);
            banks.append(b);

        return banks;

    def getTitleByUrl(self, url):
        f = self.openUrl(url);
        if f == None:
            return "";

        soup = BeautifulSoup(f);
        p = soup.find("span", class_="f_666_12").find("p");
        return SoupUtil.getStrings(p);
