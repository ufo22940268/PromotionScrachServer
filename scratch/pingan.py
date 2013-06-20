#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser

class BanksGetter(BaseGetter):
    def getName(self):
        return "平安银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://creditcard.pingan.com/cms-tmplt/creditcard/searchPreferentialActivity.do?type=&city=shenzhen&currentPage=%d";
        for page in range(1, self.getPageRange()):
            url = baseUrl % page;
            soup = self.getSoup(url);
            if not soup:
                break;

            lis = soup.find_all("tr", class_="item");
            for l in lis:
                b = Bank();
                a = l.find("a");
                title = a["title"].encode("utf-8");
                m = re.match(r"\[(.*)\]", title);
                if m:
                    b.city = m.group(1);
                b.title = re.sub(r"【.*】|\[.*\]", "", title);
                b.url = "http://creditcard.pingan.com" + a["href"].encode("utf-8");
                ds = l.contents[-2].string.encode("utf-8");
                b.endDate = date_parser.parseDashLineStyle(ds);
                banks.append(b);
        
        return banks;
