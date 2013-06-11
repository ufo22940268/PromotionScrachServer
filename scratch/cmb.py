#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
import re
import json
from time import gmtime, strftime

class CmbGetter(BaseGetter):

    def getName(self):
        return "招商银行";

    def fetchBankList(self):
        f = urllib.urlopen("http://cc.cmbchina.com/SvrAjax/PromotionChange.ashx?city=0411&type=specialsale");
        raw = f.readlines();
        strs = raw[:];
        if strs != None:
            i = strs[0].find("(");
            new = strs[0][:i] + strs[0][i + 1:];
            i = new.rfind(")");
            new = new[:i] + new[i + 1:];

        new = re.sub(r"(\w+):", r'"\1":', new);
        new = re.sub(r"\"http\"", r'http', new);
        blJo = json.loads(new)["list"];
        banks = [];
        for bJo in blJo:
            b = self.inflateBank(bJo);
            banks.append(b);
        return banks;

    def inflateBank(self, jo):
        b = Bank();
        url = jo["LinkUrl"].encode("utf-8");
        if url.find("http:") == -1:
            b.url = "http://cc.cmbchina.com" + url;
        else:
            b.url = url;

        b.title = jo["Title"].encode("utf-8");
        b.name = "招商银行";
        b.fetchTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
        return b;
