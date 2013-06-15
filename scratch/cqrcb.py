#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import json

class BanksGetter(BaseGetter):
    def getName(self):
        return "重庆农村商业银行";

    def fetchBankList(self):
        banks = [];
	for page in range(1, self.getPageRange()): 
            f = self.openUrl("http://app.cqrcb.com:81/apply/ajax/AjaxSearch?pageNo=" + str(page) + "&bianliang=0");
	    if f == None:
		break;

            root = json.loads(f.read());
            for l in root['merchantList']:
                b = Bank();
                b.url = "http://app.cqrcb.com:81/apply/ShowDetail.action?merid=" + l["merid"].encode("utf-8");
                b.title =  l["merpro"].encode("utf-8");
                banks.append(b);
	return banks;
