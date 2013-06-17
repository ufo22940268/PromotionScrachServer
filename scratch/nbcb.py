#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import SoupUtil

class BanksGetter(BaseGetter):
    def getName(self):
        return "宁波银行";

    def fetchBankList(self):
        urls = self.getUrls();
        banks = [];
        banks += self.getBankListByUrl("http://www.nbcb.com.cn/xyk/thsh/nb/index.shtml");
	return banks;

    def getUrls(self):
        urls = [];
        f = self.openUrl("http://www.nbcb.com.cn/xyk/thsh/nb/index.shtml");
        if f == None:
            return;

        soup = BeautifulSoup(f);
        lis = soup.find("div", class_="aTab subaTab").find_all("a");
        for l in lis:
            urls.append("http://www.nbcb.com.cn" + l["href"].encode("utf-8"));
        return urls;

    def getBankListByUrl(self, url):
        banks = [];
        f = self.openUrl(url);
        if f == None:
            return banks;

        soup = BeautifulSoup(f);
        urls = soup.find("tbody").find_all("a", target="_blank", href=re.compile(r"\b\d+\.shtml"));
        urls = ["http://www.nbcb.com.cn" + u["href"].encode("utf-8") for u in urls];

        for url in urls:
            b = Bank();
            b.url = url;
            b.title = self.getTitleByUrl(url);
            banks.append(b);

        return banks;

    def getTitleByUrl(self, url):
        soup = self.getSoup(url);
        if soup == None:
            return "";

        return SoupUtil.getStrings(soup.find("div", class_="shopIntroBox"));
