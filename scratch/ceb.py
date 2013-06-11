#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "光大银行";

    def fetchBankList(self):
        banks = [];
        for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://xyk.cebbank.com/home/dd/dealerList.htm?cate=&city=&=&qw=%E5%95%86%E6%88%B7%E5%90%8D%E6%88%96%E5%9C%B0%E5%9D%80&sc=&pageNo=" + str(page));

            if f == None:
                break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("div", class_="sh_list_item floatk");
	    for l in lis:
		b = Bank();
		a = l.find("a");
                b.url = "http://xyk.cebbank.com/" + l.find("a")["href"].encode("utf-8");
		b.title = l.find("div", class_="floatright sh_list_item_r").find("table").contents[-2].contents[-2].string.strip().encode("utf-8");
		banks.append(b);
	return banks;
