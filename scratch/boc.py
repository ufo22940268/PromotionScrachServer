#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

#TODO Can't find the right website.
class BanksGetter(BaseGetter):
    def getName(self):
        return "中国银行";

    def fetchBankList(self):
        pass

    def getBankListByUrl(self, url):
        banks = [];
        #f = self.openUrl("http://www.boc.cn/sdbapp/rwmerchant/1581/1586/1588/");
        #if f == None:
            #break;

        #soup = BeautifulSoup(f);
        #lis = soup.find_all("dl", class_="cont-list");
        #for l in lis:
            #b = Bank();
            #a = l.find("a");
            #b.url = "http://creditcard.ccb.com" + l.find("a", class_="more")["href"].encode("utf-8");
            #b.title = l.contents[-2].contents[-1].string.encode("utf-8").strip();
            #banks.append(b);
	#return banks;
        return banks;
