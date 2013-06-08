#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank

class CiticGetter(BaseGetter):

    def getName(self):
        return "中信银行";

    def fetchBankList(self):
        f = urllib.urlopen("http://cards.ecitic.com/youhui/shuakahuodong.shtml");
        #f = open("citic.html");
        soup = BeautifulSoup(f);
        lis = soup.find_all("li", class_="emb4 item-n");
        banks = [];
        for li in lis:
            b = Bank();
            h2 = li.find_all("h2")[0];
            b.title = h2.string.encode("utf-8");
            b.name = self.getName();
            b.url = "http://cards.ecitic.com/youhui/" +li.find("a", class_="a-h")["href"].encode("utf-8");
            banks.append(b);
        #return dict(name=self.getName(), banks=banks);
        return banks;
