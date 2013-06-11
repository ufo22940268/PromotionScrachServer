#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util

class BanksGetter(BaseGetter):
    def getName(self):
        return "农业银行";

    def fetchBankList(self):
        banks = [];
        for page in range(0, self.getPageRange()): 
            f = self.openUrl("http://www.abchina.com/services/fund/Quotes/DataService.svc/GET?id=CreditCardFilter&p=true&f=html&i=" + str(page) + "&s=5&o=1&w=0%7C-1%7C-1%7C%7C-1%7C1");

            if f == None:
                break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("div", class_="EXImageSlot");
	    for l in lis:
		b = Bank();
                b.url = "Can't find detail page.";
		b.title = l.find("span", class_="aTitle").string.strip().encode("utf-8");
		banks.append(b);

	return banks;
