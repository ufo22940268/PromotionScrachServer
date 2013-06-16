#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "建设银行";

    def fetchBankList(self):
        urls = self.getUrls();
        print "urls:", urls;
        banks = [];
        banks += getBankListByUrl("http://www.nbcb.com.cn/xyk/thsh/nb/index.shtml");
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
        f = self.openUrl(url);
        if f == None:
            return;
