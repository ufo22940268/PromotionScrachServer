#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import soup_util

class BanksGetter(BaseGetter):
    def getName(self):
        return "宁波银行";

    def fetchBankList(self):
        banks = [];
        baseUrl = "http://www.nbcb.com.cn/xyk/thtghd/index%s.shtml";
        for page in range(1, self.getPageRange()):
            url = None;
            if page == 1:
                url = baseUrl % "";
            else:
                url = baseUrl % "_" + str(page);

            soup = self.getSoup(url);
            if not soup:
                break;

            for a in soup.find("div", class_="newslist").find_all("a", class_=""):
                b = Bank();
                b.url = "http://www.nbcb.com.cn" + a["href"].encode("utf-8");
                title = soup_util.getStrings(a);
                m = re.match(r"\[(.*)\]", title);
                if m:
                    b.city = m.group(1);
                b.title = re.sub(r"\[(.*)\]|【(.*)】", "", title);
                banks.append(b);

	return banks;
