#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
import re
import json
from time import gmtime, strftime

class BanksGetter(BaseGetter):

    def getName(self):
        return "招商银行";

    def fetchBankList(self):
        banks = [];
        cities = self.getCities();
        for dic in cities:
            cityId = dic["id"];    
            cityName = dic["name"];
            url = "http://cc.cmbchina.com/SvrAjax/PromotionChange.ashx?city=%s&type=specialsale" % (cityId)
	    f = self.openUrl(url);
            if f == None:
                break;

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
            for bJo in blJo:
                b = self.inflateBank(bJo);
                b.city = cityName;
                banks.append(b);

        banks = self.correctBanks(banks);
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

    def getCities(self):
        cities = [];
        #soup = self.getSoup("http://cc.cmbchina.com/Promotion/");
        soup = BeautifulSoup(open("cmb").read());
        for a in soup.find_all("a", href=re.compile(r'javascript:GetList')):
            href = a["href"];
            m = re.match(".*\('\w+'.*'(\w+)'.*'(.*)'", href);
            if m:
                id = m.group(1).encode("utf-8");
                name = m.group(2).encode("utf-8");
                cities.append(dict(id=id, name=name));
        return cities;

    def correctBanks(self, banks):
        bd = dict();

        for b in banks:
            k = b.title + b.url;
            if not bd.get(k):
                bd[k] = b;
            else:
                bd[k].city = None;

        return bd.values();
