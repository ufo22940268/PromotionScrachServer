#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util
import re
import date_parser
import traceback

class BanksGetter(BaseGetter):
    def getName(self):
        return "农业银行";

    def fetchBankList(self):
        banks = [];
        #print self.getEndDateByUrl("http://www.abchina.com/cn/CreditCard/Promotions/BusinessActivity/201306/t20130609_352254.htm");
        for page in range(0, self.getPageRange()): 
            soup = None;
            if page == 0:
                soup = self.getSoup("http://www.abchina.com/cn/PublicPlate/ABCPromotion/default.htm");
            else:
                soup = self.getSoup("http://www.abchina.com/cn/PublicPlate/ABCPromotion/default_%d.htm" % (page,));

            if soup == None:
                return;

            lis = soup.find_all("li", class_="DotLi100");
            for l in lis:
                b = Bank();
                a = l.find("a");
                b.url = "http://www.abchina.com/cn/PersonalServices/Promotions/" + a["href"].encode("utf-8");
                b.title = a.string.encode("utf-8");
                b.endDate = self.getEndDateByUrl(b.url);
                banks.append(b);

	return banks;

    def getEndDateByUrl(self, url):
        soup = self.getSoup(url);
        if soup == None:
            return;
        
        try: 
            s = soup.find("strong", text=re.compile("活动时间".decode("utf-8"))).parent.next_sibling.next_sibling.string.encode("utf-8");
            m = re.match(".*至(.*日)", s);
            if m == None:
                return;
            else:
                return date_parser.parseChineseStyle(m.group(1));
        except:
            pass
