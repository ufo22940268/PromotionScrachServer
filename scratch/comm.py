#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util
import date_parser

FIXED_COUNT = 8;
class BanksGetter(BaseGetter):
    def getName(self):
        return "交通银行";

    def fetchBankList(self):
        banks = [];
        
        for page in range(1, FIXED_COUNT): 
            url = "http://creditcard.bankcomm.com/bcms/front/activity/ajax/search.do?tab=1&pageNo=%d&isPage=true" % (page,);
            soup = self.getSoup(url);
            if not soup:
                return banks

            lis = soup.find_all("div", class_="wzms");
            for l in lis:
                b = Bank();
                b.url = "http://creditcard.bankcomm.com" + l.next_sibling.next_sibling.find("a", class_="btnMore")["href"].encode("utf-8");
                b.title = l.find("td", class_="t2").string.encode("utf-8").strip();
                b.endDate = date_parser.parseZhiStyle(l.find("td", class_="t4").string.encode("utf-8").strip());
                banks.append(b);

	return banks;
