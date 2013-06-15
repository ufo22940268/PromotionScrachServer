#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
import util

class BanksGetter(BaseGetter):
    def getName(self):
        return "浦发银行";

    def fetchBankList(self):
        banks = [];
        cities = self.getCities();
        for cityId in cities:
            f = self.openUrl("http://service.spdbccc.com.cn/spdb/frontend/store/storeAction.do?method=searchStore&areaType_id=" + cityId + "&store_class=" + cityId);

            if f == None:
                continue;

            soup = BeautifulSoup(f);
            lis = soup.find_all("a", class_="STYLE_shanghu_new");
            for l in lis:
                b = Bank();
                href = l["href"].encode("utf-8");
                if href == "#store_list":
                    continue;
                b.url = "http://service.spdbccc.com.cn/" + href;
                titleNode = l.parent.next_sibling.next_sibling;
                if titleNode != None and titleNode.string != None:
                    b.title = titleNode.string.encode("utf-8");
                banks.append(b);

	return banks;

    def getCities(self):
        cities = [];
        f = self.openUrl("http://service.spdbccc.com.cn/spdb/frontend/store/index.jsp");
        soup = BeautifulSoup(f);
        shanghus = soup.find("select", class_="inp_shanghu").find_all("option")[1:];
        for s in shanghus:
            cities.append(s["value"].encode("utf-8"));
        return cities;

