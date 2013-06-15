#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "大连银行";

    def fetchBankList(self):
        banks = [];
	for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://www.bankofdl.com/xyk/node_107_" + str(page + 1) + ".htm");
	    if f == None:
		break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("span", class_="huang12");
	    for l in lis:
                l = l.parent;
		b = Bank();
                b.url = "http://www.bankofdl.com/xyk/" + l.find("a")["href"].encode("utf-8");
                b.title =  "".join(l.stripped_strings).encode("utf-8");
		banks.append(b);
	return banks;
