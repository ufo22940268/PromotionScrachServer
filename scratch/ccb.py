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
    def getName(self):
        return "建设银行";

    def fetchBankList(self):
        banks = [];
        url = "http://creditcard.ccb.com/favorable/activelist_%d.html"
        
        for p in range(1, FIXED_COUNT):
            soup = self.getSoup(url % p);
            if soup == None:
                break;

            anchors = soup.find_all("a", onclick=re.compile("getHelpInfo"));
            for anchor in anchors:
                b = Bank();
                b.title = anchor["title"].encode("utf-8");
                b.url = "http://creditcard.ccb.com" + anchor["href"].encode("utf-8");
                b.endDate = self.getDateByUrl(b.url);
                banks.append(b);

	return banks;

    def getDateByUrl(self, url):
        soup = self.getSoup(url);
        if soup == None:
            return None;

        s = soup.find("p").contents[-1].string.encode("utf-8");
        m = re.match(r".* ~ (.*)", s);
        return date_parser.parseChineseStyle(m.group(1));
