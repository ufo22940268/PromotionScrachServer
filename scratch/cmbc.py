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
        return "民生银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.getPageRange()): 
            print "http://creditcard.cmbc.com.cn/Ex-gratiaBusiness/ResultList.aspx?page=" + str(page);
            f = self.openUrl("http://creditcard.cmbc.com.cn/Ex-gratiaBusiness/ResultList.aspx?page=" + str(page));

            if f == None:
                break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("li", class_="nameSh");
	    for l in lis:
		b = Bank();
                b.url = "http://creditcard.cmbc.com.cn/Ex-gratiaBusiness/" + l.find("a")["href"].encode("utf-8");
		b.title = self.getTitleByUrl(b.url);

		banks.append(b);
	return banks;

    def getTitleByUrl(self, url):
        f = self.openUrl(url);
        soup = BeautifulSoup(f, from_encoding="gbk");
        return soup.find(style=re.compile(r"color:#ff0000;")).string.encode("utf-8");

