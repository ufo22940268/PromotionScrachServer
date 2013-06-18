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
        return "交通银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://creditcard.bankcomm.com/bcms/front/merchant/ajax/search.do?pageNo=" + str(page) + "&tab=1&isPage=true");

            if f == None:
                break;

	    soup = BeautifulSoup(f);
            print soup.prittify().encode("utf-8");
	    #lis = soup.find_all("div", class_="ml-item");
	    #for l in lis:
		#b = Bank();
                #b.url = "http://creditcard.bankcomm.com/" + l.find("a")["href"].encode("utf-8");
                #b.title = l.find_all("div", class_="ml-end")[-1].contents[-1].encode("utf-8")
		#banks.append(b);

	return banks;
