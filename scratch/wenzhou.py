#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser
import soup_util

FIXED_COUNT = 3;
#TODO Not finished yet.
class BanksGetter(BaseGetter):
    def getName(self):
        return "温州银行";

    def fetchBankList(self):

        #test
        print self.parseDate("http://www.wzbank.cn/credit/newsview/menu_item_id/268/page_id/375"); 
        return;
        #test
        
        banks = [];
        baseUrl = "http://www.wzbank.cn/credit/newslist/menu_item_id/268/page/%d";

        for page in range(1, FIXED_COUNT):
            url = baseUrl % page;
            soup = self.getSoup(url);
            if not soup:
                break;

            for l in soup.find("div", class_="all-news-right-wrapper").find("ul").find_all("li"):
                b = Bank();
                a = l.find("a");
                b.title = a.string.encode("utf-8");
                b.url = "http://www.wzbank.cn" + a["href"].encode("utf-8");
                banks.append(b);

	return banks;

    def parseDate(self, url):
        pass
        #soup = self.getSoup(url);
        #if not soup:
            #return;

         #for s in soup.stripped_strings;
        #m = re.match(".*至(.*日)", page);
        #if m:
            #return m.group(1);
        
