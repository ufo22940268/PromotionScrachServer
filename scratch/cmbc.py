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
        return "民生银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://creditcard.cmbc.com.cn/Ex-gratiaBusiness/ResultList.aspx?page=" + str(page));

            if f == None:
                break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("li", class_="nameSh");
	    for l in lis:
		b = Bank();
                b.url = "http://creditcard.cmbc.com.cn/Ex-gratiaBusiness/" + l.find("a")["href"].encode("utf-8");
		b.title = l.parent.find("font").string.strip().encode("utf-8");
		banks.append(b);
	return banks;
