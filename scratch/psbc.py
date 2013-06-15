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
        for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://www.psbc.com/portal/main?transName=searchShop&province=&city=&card=&shoptype=&rate=&keyvalue=%E8%BE%93%E5%85%A5%E5%95%86%E6%88%B7%E5%90%8D%E7%A7%B0%E6%88%96%E5%9C%B0%E5%8C%BA%E5%90%8D&intpage=" + str(page));

            if f == None:
                break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("div", class_="shanghu");
	    for l in lis:
		b = Bank();
                onclick = l.find("input")["onclick"];
                m = re.search(r"window\.open\('([^']*)'", onclick);
                b.url = "http://www.psbc.com/" + m.group(1).encode("utf-8");
                b.title = l.find("td", text="优惠折扣：").next_sibling.next_sibling.string.strip().encode("utf-8");
		banks.append(b);
	return banks;
