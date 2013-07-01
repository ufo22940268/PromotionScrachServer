#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util
import re

class BanksGetter(BaseGetter):
    def getName(self):
        return "中国邮政储蓄银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://www.psbc.com/portal/zh_CN/CreditCard/SpecialOffers/index%s.html";
        for page in range(0, self.getPageRange()): 
            if page == 0:
                url = baseUrl % ("",);
            else:
                url = baseUrl % ("_" + str(page),);
            soup = self.getSoup(url);
            if not soup:
                break;

            for a in soup.find("ul", class_="artic_list clearfix").find_all("a"):
                b = Bank();
                url =  a["href"].encode("utf-8");
                if re.match(r"http", url):
                    b.url = url; 
                else:
                    b.url = "http://www.psbc.com" + url;

                title = a.string.encode("utf-8");
                m = re.match("(.*)：(.*)", title);
                if not m:
                    b.title = title;
                else:
                    b.title = m.group(2);
                    b.city = m.group(1);

                banks.append(b);
            
	return banks;
