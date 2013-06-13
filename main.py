#coding=utf-8
import urllib
import json
import re
from bank import Bank
from bs4 import BeautifulSoup
import db
import util
import scratch.abc
import scratch.ccb
import scratch.ceb
import scratch.cgb
import scratch.citic
import scratch.cmbc
import scratch.cmb

ALL_BANKS = [
        scratch.abc,
        scratch.ccb,
        scratch.ceb,
        scratch.cgb,
        scratch.citic,
        scratch.cmbc,
        scratch.cmb,
        ]

def fetchCmbBanks():
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
        b = inflateBank(bJo);
        banks.append(b);
    return banks;

def fetchCiticBanks():
    #f = urllib.urlopen("http://cards.ecitic.com/youhui/shuakahuodong.shtml");
    f = open("citic.html");
    soup = BeautifulSoup(f);
    lis = soup.find_all("li", class_="emb4 item-n");
    banks = [];
    for li in lis:
        b = Bank();
        h2 = li.find_all("h2")[0];
        b.title = h2.string.encode("utf-8");
        b.name = "中信银行";
        b.link = "http://cards.ecitic.com/youhui/" +li.find("a", class_="a-h")["href"];
        banks.append(b);
    return banks;


def real(index):
    return index*2;

def temp():
    for bankEntity in ALL_BANKS:
        getter = bankEntity.BanksGetter();
        name = getter.getName();
        banks = getter.fetchBankList();
        db.insertBankName(name);
        for b in banks:
            b.name = name;
            db.insertBank(b);

if __name__ == '__main__':
    temp();
    #util.clearBankTable();

    #banks = [];
    #banks = banks  + fetchCmbBanks();
    #banks = banks  + fetchCiticBanks();
    #for b in banks:
        #db.insertBank(b);    

    #util.printBankTable();
