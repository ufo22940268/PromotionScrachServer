#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import date_parser
import re

class BanksGetter(BaseGetter):

    def getName(self):
        return "中信银行";

    def fetchBankList(self):
        f = self.openUrl("http://cards.ecitic.com/youhui/shuakahuodong.shtml");
        if f == None:
            return;

        soup = BeautifulSoup(f);
        lis = soup.find_all("li", class_="emb4 item-n");
        banks = [];
        for li in lis:
            b = Bank();
            h2 = li.find_all("h2")[0];
            b.title = h2.string.encode("utf-8");
            b.name = self.getName();
            b.url = "http://cards.ecitic.com/youhui/" +li.find("a", class_="a-h")["href"].encode("utf-8");
            ds = li.find("span", class_="date")
            if ds and ds.string:
                ds = ds.string.encode("utf-8");
                print "ds", ds
                m = re.match(r".*-(.*)", ds)
                if m: 
                    b.endDate = date_parser.parseSlashStyle(m.group(1).strip());
            banks.append(b);
        return banks;
