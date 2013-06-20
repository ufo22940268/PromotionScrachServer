#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import re
import date_parser

class BanksGetter(BaseGetter):

    def getName(self):
        return "工商银行";


    def fetchBankList(self):
        banks = [];

        #Country area.
        url1 = "http://www.icbc.com.cn/icbc/%E7%89%A1%E4%B8%B9%E5%8D%A1/%E7%BC%A4%E7%BA%B7%E6%B4%BB%E5%8A%A8/%E5%85%A8%E5%9B%BD%E4%BC%98%E6%83%A0%E6%B4%BB%E5%8A%A8%E5%88%97%E8%A1%A8.htm";
        #Local area
        url2 = "http://www.icbc.com.cn/icbc/%E7%89%A1%E4%B8%B9%E5%8D%A1/%E7%BC%A4%E7%BA%B7%E6%B4%BB%E5%8A%A8/%E5%9C%B0%E5%8C%BA%E4%BC%98%E6%83%A0%E6%B4%BB%E5%8A%A8%E5%88%97%E8%A1%A8.htm";
        banks += self.parseOuter(url1);
        banks += self.parseOuter(url2);
	return banks;


    def parseOuter(self, url):
        banks = [];
        soup = self.getSoup(url);
        if soup != None:
            trs = soup.find_all("tr", style="height:25px;");
            for tr in trs:
                a = tr.find("a");
                u = "http://www.icbc.com.cn" + a["href"].encode("utf-8");
                text = a.string.encode("utf-8");
                if text.find("“精彩活动在这里") == -1:
                    b = Bank();
                    b.url = u;
                    
                    #remove city info.
                    text = self.removeCity(text);

                    b.title = text;
                    banks.append(b);
                else:
                    #banks += self.parseInner(u);
                    pass
        return banks;

    #Inner parse not enbaled.
    def parseInner(self, url):
        banks = [];
        soup = self.getSoup(url);

        for a in soup.find("table", class_="ke-zeroborder").find_all("a"):
            b = Bank();
            b.url = a["href"].encode("utf-8");
            b.title = self.removeCity(a.string.encode("utf-8"));
            banks.append(b);
        return banks;

    def removeCity(self, s):
        return re.sub(r".+--", "", s);
