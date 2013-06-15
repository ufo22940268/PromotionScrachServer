#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "东亚银行";

    def fetchBankList(self):
        banks = [];
	for page in range(1, self.getPageRange()): 
            url = "https://ebank.hkbea.com.cn/batwtp/beaMercQuery.do?turnPageBeginPos=" + str(page);
            f = self.openUrl(url);
	    if f == None:
		break;

	    soup = BeautifulSoup(f);
	    lis = soup.find_all("div", class_="ldtconts");
	    for l in lis:
		b = Bank();
                b.url = url;
                b.title =  "".join(l.stripped_strings).encode("utf-8").replace(r"优惠信息：", "");
		banks.append(b);
	return banks;
