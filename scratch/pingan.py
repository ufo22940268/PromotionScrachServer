#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

#TODO Getting this page cost too much time.
class BanksGetter(BaseGetter):
    def getName(self):
        return "平安银行";

    def fetchBankList(self):
        banks = [];
        #cities = self.getCities();
        ##print cities
        #for city in cities:
            #for page in range(1, self.getPageRange()):
                #url ="http://creditcard.pingan.com/cms-tmplt/tehuishanghu/searchCommerceInfoByCondition.do?city=" + city + "&currentPage=" + str(page);
                #banks += self.getBankListByUrl(url);
        #banks += self.getBankListByUrl("http://creditcard.pingan.com/cms-tmplt/tehuishanghu/searchCommerceInfoByCondition.do?city=广州&currentPage=4");
        return banks;

    def getBankListByUrl(self, url):
        print url
        banks = [];
        f = self.openUrl(url)
        if f == None:
            return banks;

        soup = BeautifulSoup(f);
        lis = soup.find_all("div", class_="box shopAd");
        for l in lis:
            b = Bank();
            b.title = l.find("p", class_="zunxiangtehui").string.encode("utf-8");
            b.url = "http://creditcard.pingan.com" + l.find("a", "but pull-left")["href"].encode("utf-8");
            banks.append(b);

        return banks;

    def getCities(self):
        cities = [];
        f = self.openUrl("http://creditcard.pingan.com/cms-tmplt/tehuishanghu/searchCommerceInfoByCondition.do?city=%E4%B8%8A%E6%B5%B7");
        soup = BeautifulSoup(f);
        anchors = soup.find("div", "text_select_index").find_all("a");
        for a in anchors:
            cities.append(a.string.encode("utf-8"));
        return cities;
